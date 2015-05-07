# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FPMasukan(Document):
	pass
def invoice_func (doc,method):
	pass
	if method=="validate" :
		#check if is local is checked then FP keluaran is required and FP keluaran must be the valid one
		if doc.is_local == 1 :
			if doc.no_faktur_pajak=="" :
				frappe.throw ("""Faktur Pajak Harus di isi untuk penjualan local""")
			check=frappe.db.sql("""select no_faktur,invoice from `tabFP Masukan` where no_faktur="{0}" """.format(doc.no_faktur_pajak,doc.posting_date))
			if len(check)>0:
				frappe.throw("""Kode Faktur pajak yang di masukan telah di gunakan oleh {0}""".format(check[0][1]))
			else:
				pass
		else:
			pass
			#doc item must have HS and check it sinv item SK is valid
	elif method=="on_submit":
		#update fp value
		if doc.is_local == 1 :
			fp_masukan = frappe.get_doc({
			"doctype":"FP Masukan",
			"no_faktur":doc.no_faktur_pajak,
			"value":doc.net_total/10,
			"invoice":doc.name,
			"date":doc.posting_date,
			"is_used":0,
			"supplier":doc.supplier
			})
			fp_masukan.insert()
			fp_masukan.submit()
		else:
			pass
			#update HS & SK
	elif method=="before_cancel":
		if doc.is_local == 1 :
			#set fp doc status=2
			frappe.db.sql ("""delete from `tabFP Masukan` where no_faktur="{0}" """.format(doc.no_faktur_pajak))
		else:
			pass
	pass