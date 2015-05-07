# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns= ["Kode:Data:200","Date:Date:200","Due Date:Date:200","Nominal:Currency:200","Supplier:Link/Supplier:200","Rekening:Data:300","Remark:Data:400","Voucher:Link/Journal Entry:200","Invoice:Link/Purchase Invoice:200","Invoice Value:Currency:200","Total Invoice:Currency:200"]
	
	clause = ""
	if filters.get("sup") and filters.get("sup")!="":
		clause = """ and Supplier="{0}" """.format(filters.get("sup"))	
	data = frappe.db.sql("""select g.code,g.posting_date,g.due_date,g.nominal,g.Supplier,g.rekening,g.remark,g.voucher,jvd.against_voucher,jvd.debit from `tabJournal Entry Account` jvd join `tabJournal Entry` jv on jvd.parent=jv.name  join tabGiro g on jvd.parent = g.voucher and jvd.debit>0  where g.used="Yes"  and g.docstatus=1 and (g.due_date between "{0}" and "{1}") {2} """.format(filters.get("from_date"),filters.get("to_date"),clause),as_list=1) 
	result=[]
	prev_giro=""
	temp_total=0
	counter=0
	temp_list=[]
	for row in data :
		if prev_giro == row[0]:
			temp_total=temp_total+row[9]
			result.append(["","","","","","","","",row[8],row[9],temp_total])
			
		else:
			result.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[9]])
			temp_total=row[9]
			prev_giro = row[0]
	return columns, result
	
	

