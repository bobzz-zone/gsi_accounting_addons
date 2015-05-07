# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FPKeluaran(Document):
	pass
def get_valid_fp(doctype, txt, searchfield, start, page_len, filters):
	indent_items_sql = """
        SELECT no_faktur,period
        FROM `tabFP Keluaran`
		WHERE docstatus = 1
		AND {search_key} LIKE "{search_val}%"
		AND ISNULL(invoice)=true AND period > NOW()
		limit {start}, {page_len}
		""".format(
        start=start,
        page_len=page_len,
        search_key=searchfield,
        search_val=txt
    )
	return frappe.db.sql(indent_items_sql)

def sales_invoice_func(doc,method):
	if method=="validate" :
		#check if is local is checked then FP keluaran is required and FP keluaran must be the valid one
		if doc.is_local == 1 :
			if doc.fp_keluaran=="" :
				frappe.throw ("""Faktur Pajak Harus di isi untuk penjualan local""")
			check=frappe.db.sql("""select no_faktur from `tabFP Keluaran` where isnull(invoice)=true and  period>="{1}" and no_faktur="{0}" """.format(doc.fp_keluaran,doc.posting_date))
			if len(check)>0:
				pass
			else:
				frappe.throw("""Kode FP yang di pilih tidak valid""")
		else:
			pass
			#doc item must have HS and check it sinv item SK is valid
	elif method=="on_submit":
		#update fp value
		if doc.is_local == 1 :
			frappe.db.sql ("""update `tabFP Keluaran` set value={1},invoice="{2}",date="{3}", customer="{4}" where no_faktur="{0}" """.format(doc.fp_keluaran,(doc.net_total/10),doc.name,doc.posting_date,doc.customer))
		else:
			pass
			#update HS & SK
	elif method=="before_cancel":
		if doc.is_local == 1 :
			#set fp doc status=2
			frappe.db.sql ("""update `tabFP Keluaran` set docstatus=2 where no_faktur="{0}" """.format(doc.fp_keluaran))
		else:
			pass
	pass