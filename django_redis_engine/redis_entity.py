from django.db.models.fields import FieldDoesNotExist
from md5 import md5
import pickle

class RedisEntity(object):
	def __init__(self,e_id,connection,db_table, pkcolumn, querymeta, db_name,empty):
		self.id = e_id
		self.connection = connection
		self.db_table = db_table
		self.pkcolumn = pkcolumn
		self.querymeta = querymeta
		self.db_name = db_name
		self.empty = empty
		if not empty:
			self.data = self.connection.hgetall(get_hash_key(self.db_name,self.db_table,self.id))
		
		
	def get(self,what,value):
		
		if self.empty: return ''
		if what in self.data:
			#print self.data,self.data[what]
			return unpickle(self.data[what])
		if what == self.pkcolumn:
			return self.id
		else:
			return unpickle(self.connection.hget(get_hash_key(self.db_name,self.db_table,self.id), what))				


def split_db_type(db_type):
	#TODO move somewhere else
        try:
            db_type, db_subtype = db_type.split(':', 1)
        except ValueError:
            db_subtype = None
        return db_type, db_subtype

def get_hash_key(db_name,db_table,pk):
	return db_name+'_'+db_table+'_'+str(pk)

def get_zset_index_key(db_name,db_table,infix,column,index):
	return db_name+'_'+db_table +'_' + infix + '_' + column + '_'+index

def get_list_key(db_name,db_table,key,pk):
	return db_name+'_'+db_table+'_'+key+'_'+str(pk)


def get_set_key(db_name,db_table,key,value):
	return db_name+'_'+db_table+'_'+key+'_'+hash_for_redis(value)

def unpickle(val):
	if val is None:
		return None
	else:
		return pickle.loads(val)

def enpickle(val):
	if val is None:
		return None
	else:
		return pickle.dumps(val)


def hash_for_redis(val):
	if isinstance(val,unicode):
		return md5(val.encode('utf-8')).hexdigest()
	return md5(str(val)).hexdigest()
