// Copyright (c) 2013, Myme and contributors
// For license information, please see license.txt

frappe.query_reports["Production Actual Cost By Spk"] = {
	"filters": [
		{
			"fieldname":"fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"reqd": 1,
			"width": "60px"
		}
	]
}
