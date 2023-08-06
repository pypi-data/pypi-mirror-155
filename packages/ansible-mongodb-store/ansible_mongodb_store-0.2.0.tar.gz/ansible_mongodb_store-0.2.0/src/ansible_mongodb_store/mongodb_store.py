import bsonjs
from pymongo import MongoClient
from bson.raw_bson import RawBSONDocument
import json

def _transform_to_bson(my_data_struct):
    # Convert dict to json
    json_of_dict = json.dumps(my_data_struct)
    # Convert json to raw bsonjs
    bson_of_dict = bsonjs.loads(json_of_dict)
    # Make into a bson record
    bson_record = RawBSONDocument(bson_of_dict)
    return bson_record


def _transform_from_bson(bson_record):
    # convert the record to json
    json_record = bsonjs.dumps(bson_record.raw)
    # Now load the JSON in to a python data structure
    return json.loads(json_record)

def write_to_mongo(mongo_dict, data_to_save, data_type_key):
    '''
    Rather than have a data collection per data type I am adding a level
    to the data structure where the key name is pgroup_audit_key and the value
    will indicate the data class. So for example if we want to save
    group member type data we would save a dictionary to the structure as follows
    {
        '_id': <id>,
        'data_type': 'group_member_types',
        'saved_data': { structure that was passed in }
    }
    '''

    cluster = MongoClient(mongo_dict['mongodb_host'],
                          port=int(mongo_dict['mongodb_port']),
                          username=mongo_dict['mongodb_user'],
                          password=mongo_dict['mongodb_password'],
                          authSource=mongo_dict['mongodb_authdb'],
                          document_class=RawBSONDocument)
    db = cluster[mongo_dict['mongodb_database']]
    collection = db[mongo_dict['mongodb_collection']]
    # Now we need to add the wrapper around the data_type
    data_to_write = {"data_type": data_type_key, "saved_data": data_to_save}
    # Only one record of any given type can be saved so let's delete any
    # prior records of this same type
    collection.delete_many({"data_type": data_type_key})
    bson_record = _transform_to_bson(data_to_write)
    collection.insert_one(bson_record)


def read_from_mongo(mongo_dict, data_type_key):
    cluster = MongoClient(mongo_dict['mongodb_host'],
                          port=int(mongo_dict['mongodb_port']),
                          username=mongo_dict['mongodb_user'],
                          password=mongo_dict['mongodb_password'],
                          authSource=mongo_dict['mongodb_authdb'],
                          document_class=RawBSONDocument)
    db = cluster[mongo_dict['mongodb_database']]
    collection = db[mongo_dict['mongodb_collection']]
    # Read one record from the collection
    bson_result = collection.find_one({"data_type": data_type_key})
    if bson_result:
        return _transform_from_bson(bson_result)['saved_data']
    else:
        return None