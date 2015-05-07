# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "accounting_addons"
app_title = "Accounting Addons"
app_publisher = "Myme"
app_description = "App for additional accounting module"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "myme.technology@gmail.com"
app_version = "0.0.1"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/accounting_addons/css/accounting_addons.css"
# app_include_js = "/assets/accounting_addons/js/accounting_addons.js"

# include js, css files in header of web template
# web_include_css = "/assets/accounting_addons/css/accounting_addons.css"
# web_include_js = "/assets/accounting_addons/js/accounting_addons.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "accounting_addons.install.before_install"
# after_install = "accounting_addons.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "accounting_addons.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"accounting_addons.tasks.all"
# 	],
# 	"daily": [
# 		"accounting_addons.tasks.daily"
# 	],
# 	"hourly": [
# 		"accounting_addons.tasks.hourly"
# 	],
# 	"weekly": [
# 		"accounting_addons.tasks.weekly"
# 	]
# 	"monthly": [
# 		"accounting_addons.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "accounting_addons.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "accounting_addons.event.get_events"
# }

doc_events = {
	"Journal Entry": {
		"on_submit": "accounting_addons.giro.doctype.giro.giro.on_jv_update",
		"validate":"accounting_addons.giro.doctype.giro.giro.validate_giro",
		"before_cancel": "accounting_addons.giro.doctype.giro.giro.on_trash_jv"
	},"Sales Invoice": {
		"on_submit": "accounting_addons.accounting_addons.doctype.fp_keluaran.fp_keluaran.sales_invoice_func",
		"validate":"accounting_addons.accounting_addons.doctype.fp_keluaran.fp_keluaran.sales_invoice_func",
		"before_cancel": "accounting_addons.accounting_addons.doctype.fp_keluaran.fp_keluaran.sales_invoice_func"
	},"Purchase Invoice": {
		"on_submit": "accounting_addons.accounting_addons.doctype.fp_masukan.fp_masukan.invoice_func",
		"validate":"accounting_addons.accounting_addons.doctype.fp_masukan.fp_masukan.invoice_func",
		"before_cancel": "accounting_addons.accounting_addons.doctype.fp_masukan.fp_masukan.invoice_func"
	},"Sales Order": {
		"validate":"manufacture_costing.manufacture_costing.doctype.spk.spk.validate_new",
		"on_submit":"manufacture_costing.manufacture_costing.doctype.spk.spk.validate_new",
		"on_update": "manufacture_costing.manufacture_costing.doctype.spk.spk.validate_new"
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
	}
}
