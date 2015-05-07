// Copyright (c) 2013, Myme and contributors
// For license information, please see license.txt

frappe.query_reports["SPK Production Cost Report by Closing Voucher"] = {
	"filters": [
		{
			"fieldname":"production_actual_cost",
			"label": __("Manufacture Closing Voucher"),
			"fieldtype": "Link",
			"options": "Production Actual Cost",
			"reqd": 1,
			"width": "60px"
		}
	]
}
