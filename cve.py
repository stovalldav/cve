import json
import urllib2
import db_connect
import re

mydb,db_init = db_connect.init_db()

if db_init >0:
	
	my_vendor_list = db_connect.get_vendor_list(mydb)

	req=urllib2.Request("https://cve.circl.lu/api/browse")
	opener=urllib2.build_opener()
	f=opener.open(req)
	jData=json.loads(f.read())

	for vendor in jData["vendor"]:
		print(vendor)

		found=0

		for v_id, v_name in my_vendor_list:
			if vendor == v_name:
				found=1
			else:
				do_nothing=0
		
		if found == 0:
			db_connect.init_vendor_tab(mydb,vendor)

	my_product_list = db_connect.get_product_list(mydb)

	for v_id, v_name in db_connect.get_vendor_list(mydb):
		try:
			pReq = urllib2.Request("https://cve.circl.lu/api/browse/"+v_name)
			pOpener=urllib2.build_opener()
			fP=pOpener.open(pReq)
			pData=json.loads(fP.read())
			print(pData)

			for product in pData["product"]:
				found=0

				for v_name, v_id, p_name, p_id in my_product_list:
					if product == p_name:
						found=1
				
				if found == 0:
					db_connect.init_product_tab(mydb,product, v_id)
		except Exception as e:
			print("Exception: " +str(e))
		
	for v_name, v_id, p_name, p_id in db_connect.get_product_list(mydb):

		try:
			vReq=urllib2.Request("https://cve.circl.lu/api/search/"+v_name+"/"+p_name)
			vOpener=urllib2.build_opener()
			fV=vOpener.open(vReq)
			vData=json.loads(fV.read())
	
			my_vulns_list = db_connect.get_vulns_tab(mydb,str(p_id),str(v_id))

			for vulns in vData:
				found=0

				for vuln_id, last_modified in my_vulns_list:
					if re.escape(vulns['id']) == vuln_id and re.escape(vulns['last_modified']) == last_modified:
						found=1
				if found == 0:
					db_connect.init_vulns_tab(mydb,product, v_id, vulns)
		except Exception as e:
			print("Exception: "+str(e))

else:
	req=urllib2.Request("https://cve.circl.lu/api/browse")
	opener=urllib2.build_opener()
	f=opener.open(req)
	jData=json.loads(f.read())

	for vendor in jData["vendor"]:
		print(vendor)
		db_connect.init_vendor_tab(mydb,vendor)

	for v_id, v_name in db_connect.get_vendor_list(mydb):
		try:
			pReq = urllib2.Request("https://cve.circl.lu/api/browse/"+v_name)
			pOpener=urllib2.build_opener()
			fP=pOpener.open(pReq)
			pData=json.loads(fP.read())
			print(pData)
			for product in pData["product"]:
				db_connect.init_product_tab(mydb, product, str(v_id))
		except:
			print("URL error")
		
	for v_name, v_id, p_name, p_id in db_connect.get_product_list(mydb):
		try:
			vReq=urllib2.Request("https://cve.circl.lu/api/search/"+v_name+"/"+p_name)
			vOpener=urllib2.build_opener()
			fV=vOpener.open(vReq)
			vData=json.loads(fV.read())
	
			for vulns in vData:
				db_connect.init_vulns_tab(mydb,str(p_id),str(v_id),vulns)
		except Exception as e:
			print("Exception: "+str(e))
