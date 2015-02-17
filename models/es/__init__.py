# -*- coding: utf8 -*-
import uuid
from dateutil import parser
from datetime import datetime
from elasticsearch import Elasticsearch
from User import User
from Product import Product

class ElasticSearch(object):
	es = Elasticsearch()
	db_type="es"
	db="simbiose_challenge"
	models={"user":User,"product":Product}
	"""
		Insert function:
			Insert content in the index/type ElasticSearch.
	"""
	def insert(self, table='user', **kwargs):
		if table in self.models.keys():
			insert_query=self.models[table]
			kwargs['create_date']=datetime.now()
			kwargs['update_date']=datetime.now()
			if (table+"_id") in kwargs.keys():
				kwargs["id"]=unicode(kwargs[(table+"_id")])
				del kwargs[(table+"_id")]
			
			if not "id" in kwargs.keys():
				kwargs["id"]=unicode(uuid.uuid4())
			if len(insert_query.keys())==len(kwargs) and sorted(insert_query.keys())==sorted(kwargs.keys()):
				insert_query=insert_query(**kwargs)
				insert_query.save()
				return True
		return False

	"""
		Update function:
			Updates the "documents" in ElasticSearch.
	"""	
	def update(self, table, table_id, **kwargs):
		if table is None:
			table="user"
		if 'columns' in kwargs.keys() and type(kwargs["columns"]) is dict and len(kwargs["columns"].keys())<=len(ElasticSearch.model_keys(table).keys()) and len(kwargs["columns"].keys())>=1: 
			columns=kwargs["columns"]
			columns['update_date']=datetime.now()
			body = {
			    "doc" : columns
			}
			update=self.es.update(index=self.db, doc_type=table, id=table_id, body=body)
			return True
		return False
	"""
		Get function:
			Search all "documents" in the index/type in ElasticSearch.
	"""
	def get(self, table='user', **kwargs):	
		result=dict()
		search_response=self.es.search(index=self.db, doc_type=table, _source=True)
	 	for hit in search_response['hits']['hits']:
	 		item_hit=dict()
	 		for key, values in hit["_source"].iteritems():
		 			
		 		if 'columns' in kwargs:
		 			if key in kwargs['columns']:
		 				item_hit[key]=values	
	 			else:
	 				item_hit=hit["_source"]
	 		result[unicode(hit["_id"])]=item_hit
		return result
	# Returns the fields of a given table.
	@classmethod
	def model_keys(self, table='user'):
		return self.models[table]()