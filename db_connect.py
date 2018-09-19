import mysql.connector
import re

def init_db():
	mydb = mysql.connector.connect(
		host="localhost",
		user="cveuser@localhost",
		password="cvepass",
		database="cve",
	)

	database_already_initialized=0
	
	sql = ("SELECT COUNT(*) FROM vendor")
	db_cursor = mydb.cursor()
	db_cursor.execute(sql)
	my_count = results_list=db_cursor.fetchall()
	database_already_initialized = my_count

	return mydb, database_already_initialized	

def init_vendor_tab(db_connection, ven_name):
	sql = ("INSERT INTO vendor "
		"(name) "
		"VALUES ('"+ven_name+"')")
	db_cursor = db_connection.cursor()
	db_cursor.execute(sql)
	db_cursor.close()
	db_connection.commit()

def init_product_tab(db_connection, prod_name, vendor):
	sql = ("INSERT INTO product (name, vendor_id) VALUES ('"+prod_name+"','"+vendor+"')")
	db_cursor = db_connection.cursor()
	db_cursor.execute(sql)
	db_cursor.close()
	db_connection.commit()

def init_vulns_tab(db_connection, prod_id, ven_id, vulns):
	sql = "INSERT INTO vuln (product_id, vendor_id"
	vuln_vals = " VALUES ('"+prod_id+"'"+",'"+ven_id+"'"

	for key in vulns:
		key_str = key.replace("-","_")
		key_str = key_str.replace("references","my_references")
		sql = sql+", "+key_str
		if isinstance(vulns[key],str):
			vuln_vals=vuln_vals+",'"+re.escape(vulns[key])+"'"
		elif isinstance(vulns[key],dict):
			v_vals="{"
			for v_key in vulns[key]:
				v_vals = v_key+":"+v_vals+re.escape(vulns[key][v_key])+", "
			v_vals = v_vals+"}"
			vuln_vals=vuln_vals+",'"+re.escape(v_vals)+"'"
			
		elif isinstance(vulns[key],list):
			v_vals="{"
			for x in vulns[key]:
				v_vals = v_vals+re.escape(x)+", "
			v_vals = v_vals+"}"
			vuln_vals=vuln_vals+", '"+re.escape(v_vals)+"'"
		elif isinstance(vulns[key],float):
			vuln_vals=vuln_vals+", '"+str(vulns[key])+"'"
		elif isinstance(vulns[key],int):
			vuln_vals=vuln_vals+", '"+str(vulns[key])+"'"
		else:
			vuln_vals=vuln_vals+", '"+re.escape(str(vulns[key]))+"'"
		
	vuln_vals=vuln_vals+")"
	sql=sql+")"+vuln_vals
	
	print("SQL: "+sql)
	db_cursor=db_connection.cursor()
	db_cursor.execute(sql)
	db_cursor.close()
	db_connection.commit()

def get_vendor_list(db_connection):
	db_cursor = db_connection.cursor()
	db_cursor.execute("SELECT id, name FROM vendor")
	results_list=db_cursor.fetchall()
	return results_list
	

def get_product_list(db_connection):
	db_cursor = db_connection.cursor()
	db_cursor.execute("SELECT v.name, v.id, p.name, p.id FROM vendor v JOIN product p ON v.id=p.vendor_id")
	results_list=db_cursor.fetchall()
	return results_list

def get_vulns_list(db_connection, v_id, p_id):
	db_cursor = db_connection.cursor()
	db_cursor.execute("SELECT id, last_modified FROM vuln WHERE vendor_id="+v_id+" AND product_id="+p_id)
	results_list=db_cursor.fetchall()
	return results_list
