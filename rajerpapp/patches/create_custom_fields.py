
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	custom_fields = {
		"Quotation Item": [
			{
				"fieldname": "configuration_json",
				"fieldtype": "Code",
				"label": "Configuration JSON",
				"options": "JSON",
				"hidden": 1,
				"insert_after": "item_code"
			}
		],
		"Sales Order Item": [
			{
				"fieldname": "configuration_json",
				"fieldtype": "Code",
				"label": "Configuration JSON",
				"options": "JSON",
				"hidden": 1,
				"insert_after": "item_code"
			}
		]
	}

	create_custom_fields(custom_fields)
