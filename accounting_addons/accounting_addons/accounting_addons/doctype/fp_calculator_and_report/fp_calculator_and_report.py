# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import cstr, flt, cint

class FPCalculatorandReport(Document):
	def clear_fpk_table(self):
		self.set('fp_keluaran_list', [])
		
	def get_pending_fp_keluaran(self):
		datas = frappe.db.sql("""select no_faktur,invoice,customer,value,date,period from `tabFP Keluaran` where isnull(invoice)=false and is_used=0 and docstatus=1 order by date""")
		self.clear_fpk_table()
		total=0
		for r in datas:
			tbl_fpk = self.append('fp_keluaran_list', {})
			tbl_fpk.no_faktur = r[0]
			tbl_fpk.invoice = r[1]
			tbl_fpk.customer=r[2]
			tbl_fpk.value=r[3]
			tbl_fpk.date=r[4]
			tbl_fpk.period=r[5]
			total=r[3]+total
		self.set('total_fp_keluaran',total)
		self.set('selisih',flt(self.total_fp_keluaran)-flt(self.total_fp_masukan))
		
	def clear_fpm_table(self):
		self.set('fp_masukan_list', [])
		
	def add_pending_fp_masukan(self):
		datas = frappe.db.sql("""select no_faktur,invoice,supplier,value,date,DATE_ADD(date,INTERVAL 3 MONTH) from `tabFP Masukan` where is_used=0 and docstatus=1 and DATE_ADD(date,INTERVAL 3 MONTH) > NOW() and no_faktur ="{}" order by date;""".format(self.get('fp_masukan')))
		self.clear_fpm_table()
		total=flt(self.get('total_fp_masukan'))
		fpm = [d.no_faktur for d in self.get('fp_masukan_list')]
		for r in datas:
			if cstr(r[0]) not in fpm:
				tbl_fpk = self.append('fp_masukan_list', {})
				tbl_fpk.no_faktur = r[0]
				tbl_fpk.invoice = r[1]
				tbl_fpk.supplier=r[2]
				tbl_fpk.value=r[3]
				tbl_fpk.date=r[4]
				tbl_fpk.expiry=r[5]		
				total=r[3]+total
		self.set('total_fp_masukan',total)
		self.set('selisih',flt(self.total_fp_keluaran)-flt(self.total_fp_masukan))
	
	def get_pending_fp_masukan(self):
		datas = frappe.db.sql("""select no_faktur,invoice,supplier,value,date,DATE_ADD(date,INTERVAL 3 MONTH) from `tabFP Masukan` where is_used=0 and docstatus=1 and DATE_ADD(date,INTERVAL 3 MONTH) > NOW() order by date;""")
		self.clear_fpm_table()
		total=0
		
		for r in datas:
			tbl_fpk = self.append('fp_masukan_list', {})
			tbl_fpk.no_faktur = r[0]
			tbl_fpk.invoice = r[1]
			tbl_fpk.supplier=r[2]
			tbl_fpk.value=r[3]
			tbl_fpk.date=r[4]
			tbl_fpk.expiry=r[5]		
			total=r[3]+total
		self.set('total_fp_masukan',total)
		self.set('selisih',flt(self.total_fp_keluaran)-flt(self.total_fp_masukan))
	
	def reset_form(self):
		self.set('finish',0)
		self.set('total_fp_masukan',0)
		self.set('selisih',0)
		self.set('total_fp_keluaran',0)
		self.clear_fpm_table()
		self.clear_fpk_table()
	
	def recalculate_total(self):
		fpk=self.get('fp_keluaran_list')
		fpm=self.get('fp_masukan_list')
		tk=0
		tm=0
		for d in fpk:
			tk=tk+d.value
		for d in fpm:
			tm=tm+d.value
		self.set('total_fp_masukan',tm)
		self.set('total_fp_keluaran',tk)
		self.set('selisih',tk-tm)
	
	def summarize(self):
		self.set('finish',1)
		fpk=""
		for d in self.get('fp_keluaran_list'):
			if fpk=="" :
				fpk = """ "{}" """.format(d.no_faktur)
			else:
				fpk = """{0},"{1}" """.format(fpk,d.no_faktur)
		fpm=""
		for d in self.get('fp_masukan_list'):
			if fpm=="" :
				fpm = """ "{}" """.format(d.no_faktur)
			else:
				fpm = """{0},"{1}" """.format(fpm,d.no_faktur)
		#frappe.throw("""update `tabFP Masukan` set is_used=1 , used_date=NOW() where no_faktur IN ({})""".format(fpm))
		frappe.db.sql("""update `tabFP Keluaran` set is_used=1 , used_date=NOW() where no_faktur IN ({})""".format(fpk))
		frappe.db.sql("""update `tabFP Masukan` set is_used=1 , used_date=NOW() where no_faktur IN ({})""".format(fpm))
	pass

def get_valid_fp(doctype, txt, searchfield, start, page_len, filters):
	indent_items_sql = """
        SELECT no_faktur,invoice,supplier
        FROM `tabFP Masukan`
		WHERE docstatus = 1
		AND {search_key} LIKE "{search_val}%"
		AND is_used=0 and DATE_ADD(date,INTERVAL 3 MONTH) > NOW()
		limit {start}, {page_len}
		""".format(
        start=start,
        page_len=page_len,
        search_key=searchfield,
        search_val=txt
    )
	return frappe.db.sql(indent_items_sql)
