#!/usr/bin/env python
# -*- coding: utf8 -*-

import datetime
from dateutil import parser
from models import Cassandra, ElasticSearch

"""
	Syncdb Class:
		Her that the name of the challenge , and its function is to synchronize the supported databases.
		By default yet , supported db(databases) are Cassandra & ElasticSearch .
"""
class SyncDB(object):
	"""
	db_class=dict()
	Where is " stored " , all instances of the supported db.

	base='cql' 
	Default for comparison,
	It's just a starting point , because all db 's that are colocos are synchronized.
	"""
	db_class=dict()
	base='cql'

	"""
		Add all instance db_class.
	"""
	def __init__(self, **kwargs):
		for key, value in kwargs.iteritems():
			if hasattr(value, 'db_type'):
				self.db_class[key]=value
	
	"""
		_sync_update Function:
			This function is very important to the operation of synchronization, which gives it if there are
			updates on Cassandra or ElasticSearch , and updates the database out of dat,
			UPDATE_DATE based on the field that is present in the table / index / data / tipos of db.		
	"""
	def _sync_update(self, table, db, base=None):
		if base is None:
			base=self.base
		if hasattr(db, 'insert') and hasattr(db, 'get') and hasattr(self.db_class[base], 'insert') and hasattr(self.db_class[base], 'get'):
			db=db
			base=self.db_class[base]
			columns_models=base.model_keys(table)
			db_query=db.get(table)
			base_query=base.get(table)
			for key, value in base_query.iteritems():
				if key in db_query.keys():
					"""
					Get all records by databases,
					the fields inserted by user and also the logs.
					"""
					db_all=db_query[key]
					base_all=base_query[key]

					# Find all records set by user
					columns_models_not_logs=dict(columns_models)
					del columns_models_not_logs['create_date'], columns_models_not_logs['update_date'], columns_models_not_logs[table+"_id"]
					
					base_values = dict()
					db_values = dict()
					

					base_values, result_exec = (
						base_values, 
						[base_values.update({column:base_all[column]}) for column in columns_models_not_logs.keys()]
					)

					db_values, result_exec = (
						db_values, 
						[db_values.update({column:db_all[column]}) for column in columns_models_not_logs.keys()]
					)
					
					# if the values are different for start update
					if db_values.values()!=base_values.values():
						if not type(db_all['update_date']) is datetime.datetime:
							db_all['update_date'] = parser.parse(db_all['update_date'])
						if not type(base_all['update_date']) is datetime.datetime:
							base_all['update_date'] = parser.parse(base_all['update_date'])
						
						max_base_update=max([base_all['update_date'], db_all['update_date']])
						
						if max_base_update in base_all.values():
							db.update(table, key, columns=base_values)
							return True
						elif max_base_update in db_all.values():
							base.update(table, key, columns=db_values)
							return True
		return False

	"""
		_sync_db Function:
			Any new data Synchronizes in the "bank" outdated.
	"""
	def _sync_db(self, table, db, base=base):
		if hasattr(db, 'insert') and hasattr(db, 'get') and hasattr(self.db_class[base], 'insert') and hasattr(self.db_class[base], 'get'):
			db=db
			base=self.db_class[base]
			for key, value in base.get(table).iteritems():
				if not key in db.get(table).keys():
					value[table+"_id"]=key
					db.insert(table, **value)
	"""
		_check_sync_dbsnc_dbs Function:
			If exists update's or insert's to be made.
	"""		
	def _check_sync_dbs(self):
		if len(self.db_class)>1 and hasattr(self.db_class[self.base], 'get'):
			base=self.db_class[self.base]
			for key, item_class_instance in self.db_class.iteritems():
				for table in base.models.keys():
					if hasattr(item_class_instance, 'get') and hasattr(base, 'get'):
						sync_insert_cql=self._sync_db(table, base, key)
						sync_insert_es=self._sync_db(table, item_class_instance)	
						sync_update=self._sync_update(table, item_class_instance)	

	"""
		run Function:
			Starts all "processes", cited above there.
	"""
	def run(self):
		self._check_sync_dbs()