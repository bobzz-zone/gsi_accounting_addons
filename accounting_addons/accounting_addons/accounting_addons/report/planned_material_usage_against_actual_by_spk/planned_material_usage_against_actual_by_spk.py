# Copyright (c) 2013, Bobzz and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
def execute(filters=None):
	data = []
	spk=filters.get("spk")
	item = frappe.db.get_value("SPK",spk,"item")
	bom = get_bom_materials(item,spk)
	ste=get_real_stock_entry (spk)
	qtydata=get_produced_qty(item,spk)
	if qtydata==0:
		frappe.throw("Report tidak dapat dibuat karena data produksi untuk SPK tersebut belum ada")
	bom_modifier=flt(qtydata[1])/flt(qtydata[2])
	for d in bom:
		found=0
		for e in ste:
			if e[0]==d[0]:
				data.append([d[0],d[1],round(flt(d[2]*bom_modifier),2),e[2],round(flt(d[2]*bom_modifier),2)-e[2]])
				ste.remove(e)
				found=1
		if found==0:
			data.append([d[0],d[1],round(flt(d[2]*bom_modifier),2),0,round(flt(d[2]*bom_modifier),2)])
		
	for e in ste:
		data.append([e[0],e[1],0,e[2],0-e[2]])
		
	
	return get_columns(), data
def get_columns():
	return ["item:Data:200","name:Data:200","Planned Qty:Int:200","Actual Qty:Int:200","Different:Int:200"]
def get_bom_materials(item,spk):
	bom_materials=frappe.db.sql("""select fb.item_code,it.item_name, ifnull(sum(ifnull(fb.qty, 0)/ifnull(bom.quantity, 1)), 0) as qty , fb.stock_uom from `tabBOM Explosion Item` fb, `tabBOM` bom, `tabItem` it where bom.name = fb.parent and it.name = fb.item_code and ifnull(it.is_pro_applicable, 'No') = 'No' and ifnull(it.is_sub_contracted_item, 'No') = 'No' and fb.docstatus<2 and bom.item="{0}" and bom.spk="{1}" and bom.is_default=1 and bom.is_active=1 group by fb.item_code, fb.stock_uom order by item_code""".format(item,spk),as_list=1)
	return bom_materials

def get_real_stock_entry (spk):
	ste=frappe.db.sql("""select std.item_code,i.item_name,sum(std.qty) as "jml",std.stock_uom from `tabStock Entry Detail` std join `tabStock Entry` ste on std.parent=ste.name join tabItem i on i.name = std.item_code where ste.kode_spk="{0}" and ste.docstatus=1 and i.is_sub_contracted_item="No" and i.is_manufactured_item="No" and i.is_purchase_item="Yes" and ifnull(std.t_warehouse,1)=1 group by std.item_code,std.stock_uom order by std.item_code""".format(spk),as_list=1)
	
	return ste

def get_produced_qty(item,spk):
	qty=frappe.db.sql("""select prod.qty ,prod.produced_qty,bom.quantity from `tabProduction Order` prod join tabBOM bom on prod.bom_no=bom.name where prod.docstatus=1 and prod.kode_spk="{0}" and prod.production_item="{1}" """.format(spk,item),as_list=1)
	if len(qty)==0 or qty[0]==None:
		return 0
	return qty[0]
	
