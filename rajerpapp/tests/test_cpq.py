
import frappe
import unittest
from rajerpapp.api import calculate_estimate

class TestStoveCPQ(unittest.TestCase):
	def setUp(self):
		# Setup Data
		self.create_items()
		self.create_material_set()
		self.create_config_logic()

	def create_items(self):
		# Create RM Items
		items = [
			{"item_code": "Test Sheet 2mm", "item_group": "Raw Material", "stock_uom": "Kg", "valuation_rate": 200},
			{"item_code": "Test Pipe 25mm", "item_group": "Raw Material", "stock_uom": "Meter", "valuation_rate": 100, "weight_per_unit": 1.5}, # 1.5 kg/m
			{"item_code": "Test Product", "item_group": "Products", "stock_uom": "Nos"}
		]
		for i in items:
			if not frappe.db.exists("Item", i["item_code"]):
				frappe.get_doc({
					"doctype": "Item",
					"item_code": i["item_code"],
					"item_group": i["item_group"],
					"stock_uom": i["stock_uom"],
					"valuation_rate": i.get("valuation_rate", 0),
					"weight_per_unit": i.get("weight_per_unit", 0)
				}).insert()

	def create_material_set(self):
		if not frappe.db.exists("Stove Material Set", "Test SS 304"):
			frappe.get_doc({
				"doctype": "Stove Material Set",
				"set_name": "Test SS 304",
				"density_factor": 0.0102,
				"rate_multiplier": 1.0,
				"sheet_item": "Test Sheet 2mm",
				"round_pipe_item": "Test Pipe 25mm"
			}).insert()

	def create_config_logic(self):
		if not frappe.db.exists("Product Config Logic", {"item_code": "Test Product"}):
			frappe.get_doc({
				"doctype": "Product Config Logic",
				"item_code": "Test Product",
				"labor_formula": "weight * 10", # 10 currency per kg
				"consumables_formula": "50", # Fixed 50
				"components": [
					{
						"part_name": "Top Sheet",
						"material_source": "Sheet",
						"qty_formula": "1",
						"length_formula": "L",
						"width_formula": "W",
						"condition": ""
					},
					{
						"part_name": "Legs",
						"material_source": "Round Pipe",
						"qty_formula": "4",
						"length_formula": "H - 50", # Leg height
						"width_formula": "0",
						"condition": ""
					}
				]
			}).insert()

	def test_calculation(self):
		inputs = {
			"L": 1000,
			"W": 1000,
			"H": 1000
		}

		# Expected Weight Calc:
		# Sheet: 1000x1000 / 645.16 * 0.0102 * 1 = 1550.003 / 645.16 * ...
		# Area sq inch = 1,000,000 / 645.16 = 1550.0031
		# Weight = 1550.0031 * 0.0102 = 15.81 kg

		# Pipe: (H-50) = 950mm = 0.95m
		# Weight = 0.95 * 1.5 (kg/m) * 4 = 1.425 * 4 = 5.7 kg

		# Total Weight = 15.81 + 5.7 = 21.51 kg

		# Cost Calc:
		# Sheet Cost (Kg): 15.81 * 200 = 3162
		# Pipe Cost (Meter): 0.95 * 4 = 3.8m * 100 = 380
		# Total Material = 3542

		# Labor: 21.51 * 10 = 215.1
		# Consumables: 50
		# Total Cost = 3542 + 215.1 + 50 = 3807.1

		# Price = 3807.1 * 1.3 = 4949.23

		result = calculate_estimate("Test Product", inputs, "Test SS 304")

		print(f"Calculated Weight: {result['weight']}")
		print(f"Calculated Price: {result['price']}")

		self.assertAlmostEqual(result['weight'], 21.51, places=1)

		# Verify Stock Qty logic
		for line in result["details"]:
			if line["part"] == "Legs":
				# Should be in Meters
				# 4 legs * 0.95m = 3.8m
				self.assertAlmostEqual(line["stock_qty"], 3.8, places=2)
			if line["part"] == "Top Sheet":
				# Should be in Kg
				self.assertAlmostEqual(line["stock_qty"], 15.81, places=1)
