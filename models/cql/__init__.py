# -*- coding: utf8 -*-
import uuid
from datetime import datetime
from cqlengine.management import sync_table
from User import User
from Product import Product

class Cassandra(object):
	db_type="cql"
	models={"user":User,"product":Product}

	def __init__(self, **kwargs):
		if len(kwargs)>=1:
			for key, value in kwargs.iteritems():
				registed=self._register_model(dict({key:value}))
		else:
			for key, value in self.models.iteritems():
				registed=self._register_model(dict({key:value}))

	"""
		Insert function:
			Insert columns/fields/information in the tables.
	"""
	def insert(self, table="user", **kwargs):
		if table in self.models.keys():
			insert_query=self.models[table]()	
			kwargs["create_date"]=datetime.now()
			kwargs["update_date"]=datetime.now()
			
			if not (table+"_id") in kwargs.keys():
				kwargs[(table+"_id")]=uuid.uuid4()
			if len(insert_query)==len(kwargs) and sorted(insert_query.keys())==sorted(kwargs.keys()):
				insert_query.create(**kwargs)
				return True
		return False
	"""
		Update function:
			Updates "line's" registered in Cassandra.
	"""
	def update(self, table, table_id, **kwargs):
		if table is None:
			table="user"
		try:
			update_class=self.models[table]()
			update_query=eval("update_class.objects(%s=\"%s\")" % (table+"_id", table_id))
			if update_query.count()>=1 and 'columns' in kwargs.keys() and type(kwargs["columns"]) is dict and len(kwargs["columns"])<=len(update_class) and len(kwargs["columns"])>=1:
				kwargs["columns"]["update_date"]=datetime.now()
				update_query.update(**kwargs["columns"])
			return True
		except TypeError, e:
			raise
		return False
	"""
		Get function:
			Select the fields and certain values​​, if not determined, returns all you have in the table.
	"""
	def get(self, table='user',  **kwargs):
		result_all=dict()
		if type(kwargs) is dict and 'columns' in kwargs.keys() and type(kwargs["columns"]) is list: 
			columns=(kwargs["columns"]+[table+"_id"])
		try:
			select_query=self.models[table]().timeout(1000).objects.all()

			for data in select_query:
				result_colunm=dict()
				table_id=unicode(data[table+"_id"])
				base_dict=data.keys()
			
				if 'columns' in locals():
					base_dict=columns
				for column in base_dict:
					result_colunm[column]=data[column]
					result_all[table_id]=result_colunm
			return result_all
		except TypeError, e:
			raise
		return False
		
	"""
		_register_model Function:
			Execute a CREATE TABLE ( ... ) , in Cassadra , always performed when the new models .
	"""
	def _register_model(self, model):
		try:
			if type(model) is dict and len(model)==1:
				new_sync_model=sync_table(model.values()[0])
				self.models[model.keys()[0]]=model.values()[0]
				return self.models
		except TypeError, e:
			raise TypeError("sync_table: O modelo adicionado, está em um formado errado")
		return False
	# Returns the fields of a given table.
	@classmethod
	def model_keys(self, table='user'):
		return self.models[table]()