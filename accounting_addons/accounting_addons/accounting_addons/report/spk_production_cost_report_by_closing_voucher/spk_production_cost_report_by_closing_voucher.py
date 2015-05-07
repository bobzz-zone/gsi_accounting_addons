# Copyright (c) 2013, Bobzz and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, flt
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data_result(filters)
	return columns, data

def get_columns():
	return ["SPK:Data:100","Date:Date:200","Cutting Qty:Int:100","Cutting worker:Int:100","Cutting Total hours:Float:100","Cutting Cost:Float:200","Cutting Cost Average:Float:100","Stitching Qty:Int:100","Stitching worker:Int:100","Stitching Total hours:Float:100","Stitching Cost:Float:200","Stitching Cost Average:Float:100","Assembly Qty:Int:100","Assembly worker:Int:100","Assembly Total hours:Float:100","Assembly Cost:Float:200","Assembly Cost Average:Float:100","Monthly Cost:Float:100"]

def get_data_result(filters):
	#result = []
	result = frappe.db.sql("""SELECT car.kode_spk,car.date,car.cqty,car.cworker,car.ctime,car.ccost,car.ccost/car.cqty as "cavg",car.sqty,car.sworker,car.stime,car.scost,car.scost/car.sqty as "savg",car.aqty,car.aworker,car.atime,car.acost,car.acost/car.aqty as "aavg",car.mcost from `tabProduction Cost Detail` car join `tabProduction Cost Closing Voucher` ca on car.parent=ca.name where ca.name=%(production_actual_cost)s""",filters,as_list=1)
	
	return result
