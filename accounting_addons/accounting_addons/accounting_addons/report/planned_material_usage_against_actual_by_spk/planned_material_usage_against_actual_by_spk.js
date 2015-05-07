// Copyright (c) 2013, Myme and contributors
// For license information, please see license.txt

frappe.query_reports["Planned Material Usage against Actual by SPK"] = {
	"filters": [
		{
			"fieldname":"spk",
			"label": __("Kode SPK"),
			"fieldtype": "Link",
			"options": "SPK",
			"reqd": 1,
			"width": "60px"
		}
	]
}
