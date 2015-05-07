# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = get_columns(), get_candidate ()
	return columns, data
	
def get_candidate ():
	data = frappe.db.sql("""(SELECT "Penjualan",creation, name FROM `tabSales Order` where docstatus=0) UNION (SELECT "Surat Jalan",creation, name FROM `tabDelivery Note` where docstatus=0) UNION (SELECT "Sales Invoice",creation, name FROM `tabSales Invoice` where docstatus=0) UNION (SELECT "Pembelian",creation, name FROM `tabPurchase Order` where docstatus=0) UNION (SELECT "Penerimaan barang",creation, name FROM `tabPurchase Receipt` where docstatus=0) UNION (SELECT "Invoice pembelian",creation, name FROM `tabPurchase Invoice` where docstatus=0) UNION (SELECT "Voucher",creation, name FROM `tabJournal Entry` where docstatus=0)""",as_list=1)
		
	return data

def get_columns():
	return ["Type:Data:200","Creation Date:Date:120","File:Data:100"]

