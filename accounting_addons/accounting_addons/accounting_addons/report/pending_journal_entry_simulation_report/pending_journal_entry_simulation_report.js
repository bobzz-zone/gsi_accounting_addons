// Copyright (c) 2013, Myme and contributors
// For license information, please see license.txt

frappe.query_reports["Pending Journal Entry Simulation Report"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("company"),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), 1),
			"reqd": 1,
			"width": "60px"
		},{
			"fieldname":"account",
			"label": __("Accounts"),
			"fieldtype": "Link",
			"options": "Account",
			"reqd": 1,
			"width": "60px",
			"get_query": function() {
				var company = frappe.query_report.filters_by_name.company.get_value();
				return {
					"query": "erpnext.controllers.queries.get_account_list",
					"filters": {
						"account_type": "Bank",
						"company": company
					}
				}
			}
		}
	]
}
