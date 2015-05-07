# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns=["Kode Asset:Assets/Link:200","Nama:Data:200","Jumlah:Int:200","Keterangan:Data:400","Depresiasi method:Depreciation/Link:200","Tanggal Perolehan:Date:200","Nilai Perolehan:Currency:200","Akumulasi Penyusutan:Currency:200","Nilai Buku:Currency:200","Penyusutan Tahun Berjalan:Currency:200","Akumulasi Tahun Berjalan:Currency:200","Nilai Buku Tahun Berjalan:Currency:200"]
	depreciation = frappe.db.sql("""select posting_date from `tabAsset Depreciation` order by posting_date desc limit 0,1 """,as_list=1)
	if len(depreciation)==0 :
		frappe.throw("""No Depreciation created yet!!""")

	data=frappe.db.sql("""select a.name,a.asset_name,a.qty,a.note,a.depreciation,a.posting_date, a.asset_value, a.asset_value-d.last_book_value,d.last_book_value,a.deprecation_value,a.asset_value-d.new_book_value,d.new_book_value from tabAsset a left join `tabAsset Depreciation Record` d ON a.name = d.asset and d.posting_date="{0}" where a.docstatus=1 """.format(depreciation[0][0]),as_list=1)
	#data=frappe.db.sql("""select a.name,a.asset_name,a.qty,a.note,a.depreciation,a.posting_date, a.asset_value, a.asset_value-d.last_book_value,d.last_book_value,a.deprecation_value,a.asset_value-d.new_book_value,d.new_book_value from tabAsset a join (SELECT i1.* FROM `tabAsset Depreciation Record` AS i1 LEFT JOIN `tabAsset Depreciation Record` AS i2 ON (i1.asset = i2.asset AND i1.posting_date < i2.posting_date) WHERE i2.posting_date IS NULL and i1.posting_date>DATE_SUB(NOW(),INTERVAL 3 MONTH) ) d where a.docstatus=1 group by a.name""",as_list=1)

	#data=frappe.db.sql("""select name,asset_name,qty,note,depreciation,posting_date,asset_value,asset_value-book_value,book_value,IF(book_value-deprecation_value<0,book_value,deprecation_value),IF(book_value-deprecation_value<0,book_value,asset_value-book_value+deprecation_value),IF(book_value-deprecation_value<0,asset_value,book_value-deprecation_value) from tabAsset where docstatus=1""",as_list=1)
	
	return columns, data

