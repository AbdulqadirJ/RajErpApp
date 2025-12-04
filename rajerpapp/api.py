
import frappe
from frappe.utils import flt

@frappe.whitelist()
def calculate_estimate(item_code, inputs, material_set_name):
	"""
	Calculates the estimate price and weight for a configurable product.

	:param item_code: The Item Code of the product (e.g., "Commercial Stove")
	:param inputs: Dictionary of user inputs (L, W, H, burners, leg_count, etc.)
	:param material_set_name: Name of the Stove Material Set (e.g., "SS 304 Heavy")
	:return: Dict with price, weight, details (BOM lines)
	"""
	if isinstance(inputs, str):
		inputs = frappe.parse_json(inputs)

	# Fetch Master Docs
	material_set = frappe.get_doc("Stove Material Set", material_set_name)
	logic = frappe.get_doc("Product Config Logic", {"item_code": item_code})

	total_weight_kg = 0.0
	bom_lines = []

	# Safe Eval Context
	eval_context = {"inputs": inputs}
	for key, value in inputs.items():
		eval_context[key] = value

	# Helper to evaluate formula
	def safe_eval_formula(formula, context):
		if not formula:
			return 0
		try:
			return frappe.safe_eval(formula, context)
		except Exception as e:
			frappe.throw(f"Error evaluating formula '{formula}': {e!s}")

	for component in logic.components:
		# Check Condition
		if component.condition:
			if not safe_eval_formula(component.condition, eval_context):
				continue

		# Evaluate Dimensions
		qty = flt(safe_eval_formula(component.qty_formula, eval_context))
		length_mm = flt(safe_eval_formula(component.length_formula, eval_context))
		width_mm = flt(safe_eval_formula(component.width_formula, eval_context))

		if qty <= 0:
			continue

		row_weight = 0.0
		stock_qty = 0.0
		material_item_code = None
		stock_uom = None

		# Calculate Weight based on Type
		if component.material_source == "Sheet":
			# Formula: (Area sq inch) * Density Factor * Qty
			# Area in sq inch = (mm * mm) / 645.16
			area_sq_inch = (length_mm * width_mm) / 645.16
			row_weight = area_sq_inch * material_set.density_factor * qty
			material_item_code = material_set.sheet_item
			stock_qty = row_weight # Assuming Sheet UOM is Kg

		elif component.material_source in ["Round Pipe", "Rectangle Pipe", "Angle", "Flat", "Square Rod"]:
			# Formula: (Length m) * Weight/meter * Qty
			length_m = length_mm / 1000.0

			# Map source to field name in Material Set
			field_map = {
				"Round Pipe": "round_pipe_item",
				"Rectangle Pipe": "rect_pipe_item",
				"Angle": "angle_item",
				"Flat": "flat_item",
				"Square Rod": "square_rod_item"
			}
			field_name = field_map.get(component.material_source)
			material_item_code = getattr(material_set, field_name)

			if not material_item_code:
				frappe.throw(f"Material Item not defined for {component.material_source} in set {material_set.name}")

			# Fetch weight from Item Master
			weight_per_unit = frappe.db.get_value("Item", material_item_code, "weight_per_unit") or 0.0
			row_weight = length_m * weight_per_unit * qty

			# Determine stock qty based on UOM
			stock_uom = frappe.db.get_value("Item", material_item_code, "stock_uom")
			if stock_uom in ["Meter", "m"]:
				stock_qty = length_m * qty
			else:
				stock_qty = row_weight # Default to weight (Kg)

		elif component.material_source == "Washer":
			material_item_code = material_set.washer_item
			if not material_item_code:
				frappe.throw(f"Material Item not defined for Washer in set {material_set.name}")

			weight_per_unit = frappe.db.get_value("Item", material_item_code, "weight_per_unit") or 0.0
			row_weight = weight_per_unit * qty
			stock_qty = qty # Assuming Washer UOM is Nos, check later if Kg

		total_weight_kg += row_weight

		bom_lines.append({
			"part": component.part_name,
			"cut_size": f"{length_mm} x {width_mm}" if width_mm else f"{length_mm}",
			"qty": qty,
			"weight": row_weight,
			"stock_qty": stock_qty,
			"material_item": material_item_code
		})

	# Calculate Costs
	material_cost = 0.0
	for line in bom_lines:
		if line["material_item"]:
			# Use Valuation Rate (FIFO proxy) or Price List Rate
			rate = frappe.db.get_value("Item", line["material_item"], "valuation_rate")
			if not rate:
				rate = frappe.db.get_value("Item Price", {"item_code": line["material_item"], "price_list": "Standard Buying"}, "price_list_rate") or 0.0

			# Cost = Stock Qty * Rate
			line_cost = line["stock_qty"] * rate
			material_cost += line_cost

	# Labor and Consumables
	eval_context["weight"] = total_weight_kg

	labor_cost = safe_eval_formula(logic.labor_formula, eval_context)
	consumables_cost = safe_eval_formula(logic.consumables_formula, eval_context)

	total_cost = material_cost + labor_cost + consumables_cost
	total_cost *= material_set.rate_multiplier
	selling_price = total_cost * 1.30

	return {
		"price": selling_price,
		"weight": total_weight_kg,
		"cost": total_cost,
		"details": bom_lines
	}
