# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class AssetDepreciation(Document):
	def on_cancel(self):
		frappe.throw("""You cant cancel this document""")
	def on_submit(self):
		assets=frappe.db.sql("""select name,asset_value,book_value,deprecation_value,counter,against,account,cost_center from `tabAsset` where counter>0 and last_deprecated<="{0}" and docstatus=1 """.format(self.posting_date),as_list=1)
		#frappe.throw(assets)
		for asset in assets:
			new_value=flt(asset[2])-flt(asset[3])
			if new_value<0:
				new_value=0
			#frappe.throw("""update `tabAsset` set counter=counter-1 and book_value='{0}' and last_deprecated="{1}" where name = '{2}' """.format(new_value,self.posting_date,asset[0]))
			asset_record=frappe.get_doc({
				"doctype":"Asset Depreciation Record",
				"parent":self.name,
				"asset_depreciation":self.name,
				"posting_date":self.posting_date,
				"last_book_value":asset[2],
				"depreciation_value":asset[3],
				"new_book_value":new_value,
				"asset":asset[0]
			})
			asset_record.insert()
			
			data=[{"debit":asset[3],"credit":0,"account":asset[6],"against_account":asset[5],"name":asset[0]},
			{"debit":0,"credit":asset[3],"account":asset[5],"against_account":asset[6],"name":asset[0]}]
			from erpnext.accounts.general_ledger import make_gl_entries

			gl_map = []
			for d in data:
				if d.get("debit") or d.get("credit"):
					gl_map.append(
						frappe._dict({
							'company': self.company,
							'posting_date': self.posting_date,
							'transaction_date': self.posting_date,
							'voucher_type': self.doctype,
							'voucher_no': self.name,
							'aging_date': self.get("aging_date") or self.posting_date,
							'remarks': asset[0],
							'fiscal_year': self.fiscal_year,
							'debit': 0,
							'credit': 0,
							'cost_center':asset[7],
							'is_opening': self.get("is_opening") or "No",
							"account": d.get("account"),
							"against": d.get("against_account"),
							"debit": flt(d.get("debit")),
							"credit": flt(d.get("credit"))
						})
					)

			if gl_map:
				make_gl_entries(gl_map, 0,0)
			asset_record.submit()
			
			frappe.db.sql("""update `tabAsset` set counter=counter-1 , book_value='{0}' , last_deprecated="{1}" where name = '{2}' """.format(new_value,self.posting_date,asset[0]))
	


