# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Asset(Document):
	def validate(self):
		self.book_value=self.asset_value
		val=frappe.get_doc("Depreciation", self.depreciation)
		self.counter=val.periode*12
		self.deprecation_value=round(self.asset_value/self.counter,0)
		self.last_deprecated=self.posting_date
	
	def stop_asset(self):
		frappe.db.sql("""update tabAsset set counter=0 , book_value=0,docstatus=2,sell_voucher="{}",sell_date="{}" where name="{}" """.format(self.sell_voucher,datetime.date.today().strftime('%Y-%m-%d'),self.name))
		self.docstatus = 2
		self.counter=0
		self.book_value=0
		self.sell_date=datetime.date.today().strftime('%Y-%m-%d')
