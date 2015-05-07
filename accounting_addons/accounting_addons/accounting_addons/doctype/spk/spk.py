# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import datetime
from frappe.utils import cint
import re
from frappe.model.document import Document

class SPK(Document):
	pass
def delivery_note(doc,method):
	pass

def sales_invoice(doc,method):
	pass

def validate_new(doc,method):
	chk_dupl_itm = []
	if method=="validate":
		a=datetime.date.today().strftime('%y')
		year=cint(a)
		
		if year == 99 :
			b = "00"
			c = "01"
		else:
			if year+1 <10:
				a="0{0}".format(year+1)
			else:
				a=year+1
			if year+2 < 10:
				b="0{0}".format(year+2)
			else:
				a=year+2
		regex=re.compile("(GW|GS|GF|GM)({0}|{1}|{2}){3}".format(year,year+1,year+2,"[0-9]{4}"))
		for d in doc.get('items'):
			if not regex.match(d.kode_spk) :
				frappe.throw(_("Format Kode spk {0} salah, format 2 digit kode musim + 2 digit tahun + 4 digit nomor urut").format(d.kode_spk))
			elif frappe.db.get_value("SPK", {"kode_spk": d.kode_spk}):
				frappe.throw(_("Kode spk {0} telah terpakai").format(d.kode_spk))
			else :
				if d.kode_spk in chk_dupl_itm:
					frappe.throw(_("Kode SPK {0} has been entered twice").format(d.kode_spk))
				else:
					chk_dupl_itm.append(d.kode_spk)
	if method=="on_submit":
		for d in doc.get('items'):
			record = frappe.get_doc({
					"doctype":"SPK",
					"kode_spk":d.kode_spk,
					"item":d.item_code,
					"order_qty":d.qty,
					"fiscal_year":doc.get("fiscal_year"),
					"sales_order":doc.get("name"),
					"order_date":doc.get("transaction_date")
			})
			record.insert(ignore_permissions=True)
			record.submit()
	

