# Copyright (c) 2013, Bobzz and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = ["Kode SPK:Data:200","Item Code:Link/Item:200","Sales Order:Link/Sales Order:200","Order Qty:Int:100","Order Value:Currency:200","Delivery Note:Link/Delivery Note:200","Delivered Qty:Int:100","Delivered Value:Currency:200","Invoice:Link/Sales Invoice:200","Billed Qty:Int:100","Billed Value:Currency:200"]
	result=frappe.db.sql("""
select s.kode_spk , s.item,s.sales_order ,soi.qty,soi.base_amount,
	ifnull(dni.parent,""),ifnull(dni.qty,0),ifnull(dni.base_amount,0),
	ifnull(sii.parent,""),ifnull(sii.qty,0),ifnull(sii.base_amount,0) 

from tabSPK s 
	left join `tabSales Order Item` soi on soi.parent = s.sales_order and soi.kode_spk=s.kode_spk and soi.item_code=s.item and soi.docstatus=1
	left join `tabDelivery Note Item` dni on dni.against_sales_order = s.sales_order and dni.item_code=s.item and dni.kode_spk=s.kode_spk and dni.docstatus=1
	left join `tabSales Invoice Item` sii on sii.kode_spk=s.kode_spk and sii.sales_order=s.sales_order and sii.item_code=s.item and sii.docstatus=1

where s.docstatus=1 and ifnull(sii.docstatus,1)=1 and ifnull(dni.docstatus,1)=1""",as_list=1)
	cur_spk=""
	kode_item=""
	cur_so=[]
	cur_dn=[]
	cur_in=[]
	for row in result:
		if cur_spk=="":
			cur_spk=row[0]
			kode_item=row[1]
		if not cur_spk==row[0]:
			a=len(cur_so)
			b=len(cur_dn)
			c=len(cur_in)
			max=c
			if a>=b and a>=c:
				max=a
			elif b>=a and b>=c:
				max=b
			for counter in range(0,max):
				so_no=""
				so_qty=""
				so_val=""
				if counter>0:
					cur_spk=""
					kode_item=""
				if counter < a:
					sod=cur_so[counter]
					so_no=sod[0]
					so_qty=sod[1]
					so_val=sod[2]
				dn_no=""
				dn_qty=""
				dn_val=""
				if counter < b:
					dnd=cur_dn[counter]
					dn_no=dnd[0]
					dn_qty=dnd[1]
					dn_val=dnd[2]
				in_no=""
				in_qty=""
				in_val=""
				if counter < c:
					ind=cur_in[counter]
					in_no=ind[0]
					in_qty=ind[1]
					in_val=ind[2]
				data.append([cur_spk,kode_item,so_no,so_qty,so_val,dn_no,dn_qty,dn_val,in_no,in_qty,in_val])
			cur_so=[]
			cur_dn=[]
			cur_in=[]
			cur_spk=row[0]
			kode_item=row[1]
		if not [row[2],row[3],row[4]] in cur_so:
			cur_so.append([row[2],row[3],row[4]])
		if not [row[5],row[6],row[7]] in cur_dn:
			cur_dn.append([row[5],row[6],row[7]])
		if not [row[8],row[9],row[10]] in cur_in:
			cur_in.append([row[8],row[9],row[10]])
		
		#data.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]])
		
	return columns, data


	

