// Copyright (c) 2013, Myme and contributors
// For license information, please see license.txt

frappe.query_reports["Giro Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("Due Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default":  frappe.datetime.add_months(frappe.datetime.get_today(), 1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"sup",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier",
			"width": "60px"
		}
	]
}
