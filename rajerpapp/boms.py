
import frappe
from frappe.utils import flt

def create_custom_bom(doc, method):
	"""
	On Sales Order Submit, check for items with configuration_json and create specific BOMs.
	"""
	for item in doc.items:
		if item.configuration_json:
			try:
				config = frappe.parse_json(item.configuration_json)
				if not config or not config.get("details"):
					continue

				# Generate BOM Name
				bom_name = f"BOM-{doc.name}-{item.item_code}-{item.idx}"

				# Check if BOM exists
				if frappe.db.exists("BOM", {"item": item.item_code, "name": bom_name}):
					continue

				# Create BOM
				bom = frappe.new_doc("BOM")
				bom.item = item.item_code
				bom.is_default = 0
				bom.is_active = 1
				bom.quantity = 1
				bom.currency = doc.currency
				bom.rm_cost_as_per = "Valuation Rate"

				material_map = {}
				cut_list_note = "<b>Cut List:</b><br>"

				for line in config.get("details", []):
					material = line.get("material_item")
					if not material:
						continue

					# Use stock_qty if calculated, otherwise fallback to weight
					qty = flt(line.get("stock_qty"))
					if qty == 0:
						qty = flt(line.get("weight"))

					if material not in material_map:
						material_map[material] = 0.0
					material_map[material] += qty

					cut_list_note += f"- {line.get('part')}: {line.get('cut_size')} (Qty: {line.get('qty')})<br>"

				for material, qty in material_map.items():
					bom.append("items", {
						"item_code": material,
						"qty": qty,
						"uom": frappe.db.get_value("Item", material, "stock_uom") or "Kg"
					})

				bom.save(ignore_permissions=True)
				bom.submit()

				if frappe.get_meta("Sales Order Item").has_field("bom_no"):
					frappe.db.set_value("Sales Order Item", item.name, "bom_no", bom.name)

				frappe.get_doc({
					"doctype": "Comment",
					"comment_type": "Info",
					"reference_doctype": "Sales Order",
					"reference_name": doc.name,
					"content": f"BOM Created for Row {item.idx}: {bom.name}<br>{cut_list_note}"
				}).insert(ignore_permissions=True)

			except Exception as e:
				frappe.log_error(f"Error creating Custom BOM for SO {doc.name}: {e!s}")
				frappe.msgprint(f"Warning: Failed to generate custom BOM for {item.item_code}. Check Error Log.")
