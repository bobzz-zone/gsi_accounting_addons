# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, cstr, flt
import datetime
from frappe import _
from frappe.model.document import Document

class ProductionCostClosingVoucher(Document):
	def on_cancel (self):
		frappe.db.sql("""delete from `tabProduction Cost Detail` where parent = %(parent)s """,{"parent":self.name})
	def on_submit(self):
		last_transaction = frappe.get_list("Production Cost Closing Voucher",
			fields=["posting_date"],
			filters = {
				"posting_date": ("<=", self.posting_date),
				"name": ("!=", self.name),
				"docstatus": ("=", 1)
			})
		isFirst = 1
		from_date="2001-01-01"
		if last_transaction :
			isFirst=0
			from_date=last_transaction[0].posting_date
		date_1 = datetime.datetime.strptime(from_date, "%Y-%m-%d")
		from_date = date_1 + datetime.timedelta(days=1)
		to_date = self.posting_date
		filters={"from_date":from_date,"to_date":to_date}
		#to_date="2014-11-11"
		monthly=self.get_monthly_cost(filters)
		
		time=self.get_work_timelog_data(filters)
		production=self.get_production_data(filters)
		self.summarize(time,production,monthly)
	
	def summarize(self,time,production,monthly):
		cuttingQty=0
		assemblyQty=0
		stitchingQty=0	
		totalCuttingQty=0
		totalAssemblyQty=0
		totalStitchingQty=0
		year=0
		dateofyear=0
		spk=[]
		curspk=""
		i=0
		str=""
		totalQtyOfAll=0
		date=""
		result=[]
		bahan=0
		for data in production:
			totalQtyOfAll+=data.get("produced_qty")
			if year==0 and dateofyear==0:
				year=data.get("year")
				dateofyear=data.get("tgl")
				curspk=data.get("kode_spk")
				date=data.get("posting_date")
			if year==data.get("year") and dateofyear==data.get("tgl"):
				
				if curspk==data.get("kode_spk"):
					bahan+=data.get("bahan")
					if data.get("category")=="Stitching" :
						stitchingQty+=data.get("produced_qty")
						totalStitchingQty+=data.get("produced_qty")
					if data.get("category")=="Assembly" :
						assemblyQty+=data.get("produced_qty")
						totalAssemblyQty+=data.get("produced_qty")
					if data.get("category")=="Cutting" :
						cuttingQty+=data.get("produced_qty")
						totalCuttingQty+=data.get("produced_qty")
				else:
					spk.append([curspk,cuttingQty,stitchingQty,assemblyQty,date,bahan])
					cuttingQty=0
					assemblyQty=0
					stitchingQty=0
					curspk=data.get("kode_spk")
					bahan=data.get("bahan")
					if data.get("category")=="Stitching" :
						stitchingQty=data.get("produced_qty")
						totalStitchingQty+=data.get("produced_qty")
					if data.get("category")=="Assembly" :
						assemblyQty=data.get("produced_qty")
						totalAssemblyQty+=data.get("produced_qty")
					if data.get("category")=="Cutting" :
						cuttingQty=data.get("produced_qty")
						totalCuttingQty+=data.get("produced_qty")
			else:
				spk.append([curspk,cuttingQty,stitchingQty,assemblyQty,date,bahan])
				for row in spk:
					flag=1
					if i>=len(time):
						i=len(time)-1
					while flag==1 and i<len(time):
						if time[i][0]==year and time[i][1]==dateofyear:
							flag=0
						elif time[i][0]>year or time[i][1]>dateofyear:
							flag=2
						else:
							i+=1
					cHours=0
					cPayment=0
					#cAvg=0
					sHours=0
					sPayment=0
					#sAvg=0
					aHours=0
					aPayment=0
					#aAvg=0
					if flag==0 and row[1]>0 and totalCuttingQty>0:
						cHours=(float(row[1])*float(time[i][4]))/float(totalCuttingQty)
						cPayment=(float(row[1])*float(time[i][5]))/float(totalCuttingQty)
						#cAvg=float(cPayment)/float(row[1])
					if flag==0 and row[2]>0 and totalStitchingQty>0:
						sHours=(float(row[2])*float(time[i][7]))/float(totalStitchingQty)
						sPayment=(float(row[2])*float(time[i][8]))/float(totalStitchingQty)
						#sAvg=float(sPayment)/float(row[2])
					if flag==0 and row[3]>0 and totalAssemblyQty>0:
						aHours=(float(row[3])*float(time[i][10]))/float(totalAssemblyQty)
						aPayment=(float(row[3])*float(time[i][11]))/float(totalAssemblyQty)
						#aAvg=float(aPayment)/float(row[3])
					cWork=0
					sWork=0
					aWork=0
					#frappe.throw("compare {0} with {1} is resulting {2} with flag {3} from index {4}".format(row[4],time[i][2],row[4]==time[i][2],flag,i))
					if row[4]==time[i][2]:
						cWork=time[i][3]
						sWork=time[i][6]
						aWork=time[i][9]
					#result.append([row[0],row[4],row[1],cWork,cHours,cPayment,cAvg,row[2],sWork,sHours,sPayment,sAvg,row[3],aWork,aHours,aPayment,aAvg])
					result.append([row[0],row[4],row[1],cWork,cHours,cPayment,row[2],sWork,sHours,sPayment,row[3],aWork,aHours,aPayment,row[5]])
				spk=[]
				bahan=0
				cuttingQty=0
				assemblyQty=0
				stitchingQty=0
				totalCuttingQty=0
				totalAssemblyQty=0
				totalStitchingQty=0
				year=data.get("year")
				dateofyear=data.get("tgl")
				curspk=data.get("kode_spk")
				date=data.get("posting_date")
				bahan=data.get("bahan")
				if data.get("category")=="Stitching" :
					stitchingQty=data.get("produced_qty")
					totalStitchingQty+=stitchingQty
				if data.get("category")=="Assembly" :
					assemblyQty=data.get("produced_qty")
					totalAssemblyQty+=assemblyQty
				if data.get("category")=="Cutting" :
					cuttingQty=data.get("produced_qty")
					totalCuttingQty+=cuttingQty
		
		if len(production)>0 :
			spk.append([curspk,cuttingQty,stitchingQty,assemblyQty,date,bahan])
			
			
			#frappe.throw("{} total cutting {} total sticing {} total assembly {}".format(spk,totalCuttingQty,totalStitchingQty,totalAssemblyQty))
			#frappe.throw(spk)
			for row in spk:
				flag=1
				if i>=len(time):
					i=len(time)-1
				while flag==1 and i<len(time):
					if time[i][0]==year and time[i][1]==dateofyear:
						flag=0
					elif time[i][0]>year or time[i][1]>dateofyear:
						flag=2
					else:
						i+=1
				cHours=0
				cPayment=0
				#cAvg=0
				sHours=0
				sPayment=0
				#sAvg=0
				aHours=0
				aPayment=0
				#aAvg=0
				if flag==0 and row[1]>0 and totalCuttingQty>0:
					cHours=(float(row[1])*float(time[i][4]))/float(totalCuttingQty)
					cPayment=(float(row[1])*float(time[i][5]))/float(totalCuttingQty)
					#cAvg=float(cPayment)/float(row[1])
				if flag==0 and row[2]>0 and totalStitchingQty>0:
					sHours=(float(row[2])*float(time[i][7]))/float(totalStitchingQty)
					sPayment=(float(row[2])*float(time[i][8]))/float(totalStitchingQty)
					#sAvg=float(sPayment)/float(row[2])
				if flag==0 and row[3]>0 and totalAssemblyQty>0:
					aHours=(float(row[3])*float(time[i][10]))/float(totalAssemblyQty)
					aPayment=(float(row[3])*float(time[i][11]))/float(totalAssemblyQty)
					#aAvg=float(aPayment)/float(row[3])
				cWork=0
				sWork=0
				aWork=0
				if date==row[4]:
					cWork=time[i][3]
					sWork=time[i][6]
					aWork=time[i][9]
				#result.append([row[0],row[4],row[1],cWork,cHours,cPayment,cAvg,row[2],sWork,sHours,sPayment,sAvg,row[3],aWork,aHours,aPayment,aAvg])
				result.append([row[0],row[4],row[1],cWork,cHours,cPayment,row[2],sWork,sHours,sPayment,row[3],aWork,aHours,aPayment,row[5]])
		
		self.generate_monthly_cost(result,monthly,totalQtyOfAll)
	
	def generate_monthly_cost(self,data,monthlyCost,totalQty):
		if totalQty is None:
			totalQty=0
		if monthlyCost is None:
			monthlyCost=0
		
		if totalQty==0 or monthlyCost==0:
			pcost=0
		else:
			pcost=float(monthlyCost)/float(totalQty)
			
		for row in data:
			
			record = frappe.get_doc({
				"doctype":"Production Cost Detail",
				"production_actual_cost":self.name,
				"date":row[1],
				"kode_spk":row[0],
				"parent":self.name,
				"cqty":row[2],
				"cworker":row[3],
				"ctime":row[4],
				"ccost":row[5],
				"sqty":row[6],
				"sworker":row[7],
				"stime":row[8],
				"scost":row[9],
				"aqty":row[10],
				"aworker":row[11],
				"atime":row[12],
				"acost":row[13],
				"mcost":(float(row[2])+float(row[6])+float(row[10]))*pcost,
				"bahan":row[14]
			})
			record.insert()
			record.submit()
		
	

	def get_work_timelog_data(self,filters):
		timelog = frappe.db.sql("""SELECT Year(posting_date) as "year",DAYOFYEAR(posting_date) as "tgl",posting_date, sum(cwork),sum(ctime),sum(ccost),sum(swork),sum(stime),sum(scost),sum(awork),sum(atime),sum(acost) from `tabProduction Log` where docstatus=1 and date between %(from_date)s and %(to_date)s group by posting_date order by posting_date""",filters,as_list=1)
		
		return time

	def get_production_data(self,filters):
		production_data = frappe.db.sql("""SELECT Year(STE.posting_date) as "year",DAYOFYEAR(STE.posting_date) as "tgl",prod.kode_spk,prod.category,prod.production_item,prod.name ,SUM(IF(STD.s_warehouse is NULL,1,0)*STD.qty) as "produced_qty",STE.posting_date, sum(IF(STD.t_warehouse is NULL,IF(i.is_manufactured_item="no",1,0),0)*STD.amount) as "bahan" FROM `tabProduction Order` prod JOIN `tabStock Entry` STE on STE.production_order=prod.name JOIN `tabStock Entry Detail` STD on STD.parent=STE.name JOIN `tabItem` i ON STD.item_code=i.name WHERE prod.docstatus=1 and STE.docstatus=1 and STD.docstatus=1 and STE.posting_date between %(from_date)s and %(to_date)s group by STE.posting_date,prod.kode_spk,prod.category order by STE.posting_date,prod.kode_spk,prod.category""",filters,as_dict=1)
		
		return production_data
		
	def get_monthly_cost(self,filters):
		
		monthly_cost=frappe.db.sql("""SELECT sum(ifnull(debit,0)-ifnull(credit,0)) as total from `tabJournal Voucher Detail` jvd JOIN `tabJournal Voucher` jv on jvd.parent=jv.name where jvd.docstatus=1 and jv.docstatus=1 and (jvd.account like "522%" or jvd.account like "523%") and jv.posting_date between "{}" and "{}" group by NULL""".format(filters.get("from_date"),filters.get("to_date")),as_list=1)
		
		if monthly_cost and monthly_cost[0]:
			return monthly_cost[0][0]
		return 0
