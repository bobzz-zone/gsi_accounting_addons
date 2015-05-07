# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Giro(Document):
	pass
def on_jv_update(doc,method):
	if doc.giro:
		frappe.db.sql("""update tabGiro set used="Yes"  where name="{0}" """.format(doc.giro))
						

def validate_giro(doc,method):
	old=frappe.db.sql("""select giro from `tabJournal Entry` where name="{0}" """.format(doc.name),as_list=1)

	if doc.giro :
		if doc.remark==None or doc.giro_value==None or doc.giro_date==None or doc.supplier==None or doc.giro_remark =="" or doc.giro_value==0 or doc.giro_value=="" or doc.giro_date=="" or doc.rekening =="" or doc.supplier=="" :
			frappe.throw("""Please fill all Giro Data for use Giro""")
		
		if old and len(old)>0:
			old_giro=old[0]
			if old_giro[0]==doc.giro :
				pass
			else :
				vald=frappe.db.sql(""" select used from tabGiro where docstatus=1 and name="{0}" """.format(doc.giro),as_list=1)
				
				if vald and len(vald)>0:
					if vald[0][0]=='No':
						#frappe.throw("""update tabGiro set used="Pending",supplier="{0}",rekening="{1}",remark="{2}",nominal="{3}",voucher="{5}" , posting_date="{6}",due_date="{7}"  where name="{4}" """.format(doc.supplier,doc.rekening,doc.giro_remark,doc.giro_value,doc.giro,doc.name,doc.posting_date,doc.giro_date))
						frappe.db.sql("""update tabGiro set used="Trash"  where name="{0}"; """.format(old_giro[0]))
						#frappe.throw(""" a """)
						frappe.db.sql("""update tabGiro set used="Pending",supplier="{0}",rekening="{1}",remark="{2}",nominal="{3}",voucher="{5}" , posting_date="{6}",due_date="{7}"  where name="{4}" ;""".format(doc.supplier,doc.rekening,doc.giro_remark,doc.giro_value,doc.giro,doc.name,doc.posting_date,doc.giro_date))
						
					else:
						doc.giro=old_giro[0]
						frappe.throw("""Giro already used, and giro cant be used twice""")
				else :
					doc.giro=old_giro[0]
					frappe.throw("""Giro not found""")
		else:
			vald=frappe.db.sql(""" select used from tabGiro where docstatus=1 and name="{0}" """.format(doc.giro),as_list=1)
			if vald and len(vald)>0:
				if vald[0][0]=='No':
					frappe.db.sql("""update tabGiro set used="Pending",supplier="{0}",rekening="{1}",remark="{2}",nominal="{3}",voucher="{5}" , posting_date="{6}",due_date="{7}"  where name="{4}" ;""".format(doc.supplier,doc.rekening,doc.giro_remark,doc.giro_value,doc.giro,doc.name,doc.posting_date,doc.giro_date))
				else:
					doc.giro=""
					frappe.throw("""Giro already used, and giro cant be used twice""")
			else :
				frappe.throw("""Giro not found""")
	else:
		if old and len(old)>0:
			old_giro=old[0]
			frappe.db.sql("""update tabGiro set used="Trash"  where name="{0}" """.format(old_giro[0]))
		
		
def on_trash_jv(doc,method):
	if doc.giro :
		frappe.db.sql("""update tabGiro set used="Cancelled" where used="Yes" and voucher="{0}" and name="{1}" """.format(doc.name,doc.giro))

