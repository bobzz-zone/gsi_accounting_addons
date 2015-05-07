# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, flt
from frappe import _
from erpnext.accounts.utils import (get_balance_on)
def execute(filters=None):
	columns, data = [], []
	data=process_data(get_candidate (filters),filters)
	columns=get_columns()
	return columns, data

def get_candidate (filters):
	voucher_data = frappe.db.sql("""SELECT jv.posting_date, jv.name,ifnull(jv.user_remark,'-'),ifnull(jvd.debit,0),ifnull(jvd.credit,0), if(jv.docstatus=1,'Confirmed','Pending') as 'status' FROM `tabJournal Entry` jv JOIN `tabJournal Entry Account` jvd on jv.name=jvd.parent WHERE jv.docstatus=0 and jvd.docstatus<2 and jv.posting_date <= %(to_date)s and jvd.account= %(account)s and jv.company=%(company)s  order by jv.docstatus desc,jv.posting_date , jv.name""",filters,as_list=1)
		
	return voucher_data

def get_columns():
	return ["Posting Date:Date:120","Voucher:Data:100","Remark:Data:200","Saldo awal:Currency:120","Debit:Currency:120","Credit:Currency:120","Saldo akhir:Currency:120","Status:Data:100"]
	
def process_data(data,filters):
	result=[]
	initialBalance=get_balance_on(filters["account"],filters["to_date"])
	
	for row in data:
		
		endsaldo=initialBalance+(flt(row[3])-flt(row[4]))
		result.append([row[0],row[1],row[2],initialBalance,row[3],row[4],endsaldo,row[5]])
		initialBalance=endsaldo
	return result
