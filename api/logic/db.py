import json
import mysql.connector as mariadb
import traceback
from uuid import uuid4
from datetime import datetime

def get_connection():
	c = mariadb.connect(user='appuser', host='db', port='3306', password='apppwd', database='crudappdb')

	if c.is_connected():
		return c
	else:
		raise Exception('Unable to connect to database')

def read_food(id=None):
	sqlstr = 'SELECT * FROM foods'

	if id:
		sqlstr += ' WHERE id=\'{0}\''.format(id)

	try:
		db = get_connection()
		cursor = db.cursor()
		cursor.execute(sqlstr)
		l = cursor.fetchall()
		resp = []

		for d in l:
			resp.append({
				'id': d[0],
				'name': d[1],
				'date': d[2],
			})

		return resp
	except Exception as e:
		traceback.print_exc()
		raise e
	finally:
		db.close()

def add_food(food):
	if not food:
		raise Exception('Food name parameer is mandatory')

	sqlstr = 'INSERT INTO foods VALUES (\'{0}\', \'{1}\', \'{2}\')'.format(str(uuid4()), food, datetime.now().strftime('%Y-%m-%d'))

	try:
		print(sqlstr)
		db = get_connection()
		db.cursor().execute(sqlstr)
		db.commit()
	except Exception as e:
		traceback.print_exc()
		raise e
	finally:
		db.close()
