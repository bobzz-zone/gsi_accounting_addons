# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
def execute(filters=None):
	columns=["Delivery Note:Delivery Note/Link:200","DN Total item:Currency:200","PPN(10%) DN:Currency:200","LPB Total:Currency:200","Total Billed Item:Currency:200","PPN(10%) INV:Currency:200","Invoice Total:Currency:200","Total item Diff:Currency:200","Tax Diff:Currency:200","Total Diff:Currency:200"]
	data = frappe.db.sql("""select pi.parent,sum(ifnull(pi.amount,0)) as 'dn' , sum(ifnull(ii.amount,0)) as 'inv',ifnull(dn.other_charges_total,0),ifnull(si.other_charges_total,0) from `tabDelivery Note Item` pi left join `tabSales Invoice Item` ii on pi.parent=ii.delivery_note Join `tabDelivery Note` dn on dn.name=pi.parent left join `tabSales Invoice` si on si.name=ii.parent where ifnull(ii.docstatus,1)=1 and pi.docstatus=1 GROUP BY pi.parent,ii.delivery_note,ii.parent ORDER BY pi.parent desc LIMIT 0,100 """,as_list=1)
	result=[]
	for d in data:
		
		result.append([d[0],d[1],d[3],d[1]+d[3],d[2],d[4],d[2]+d[4],d[1]-d[2],d[3]-d[4],d[1]-d[2]+d[3]-d[4]])
	#frappe.throw(result)
	return columns, result
