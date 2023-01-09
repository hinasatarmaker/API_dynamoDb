import file1 as dynamodb
from flask import Flask
from flask import request
import serverless_wsgi
from boto3 import resource
import os


AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
REGION_NAME = "eu-west-1"
resource = resource(
   'dynamodb',
   aws_access_key_id     = AWS_ACCESS_KEY_ID,
   aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
   region_name           = REGION_NAME
)
# function for creating table
def create_table_movie():   
   table = resource.create_table(
       TableName = 'Movie', # Name of the table
       KeySchema = [
           {
               'AttributeName': 'id',
               'KeyType'      : 'number' #RANGE = sort key, HASH = partition key
           }
       ],
       AttributeDefinitions = [
           {
               'AttributeName': 'id', # Name of the attribute
               'AttributeType': 'N'   # N = Number (B= Binary, S = String)
           }
       ],
       ProvisionedThroughput={
           'ReadCapacityUnits'  : 10,
           'WriteCapacityUnits': 10
       }
   )
   return table

MovieTable = resource.Table('Movie')

# function for add items to table
def write_to_movie(id, title, director):
    response = MovieTable.put_item(
        Item = {
            'id'     : id,
            'title'  : title,
            'director' : director
        }
   )
    return response

# function for get items from table
def read_from_movie(id):
    response = MovieTable.get_item(
       Key = {
           'id'     : int(id)
       }
    )
    return response

# function for udate items in table
def update_in_movie(id, data:dict):
 
   response = MovieTable.update_item(
       Key = {
           'id': int(id)
       },
       AttributeUpdates={
           'title': {
               'Value'  : data['title'],
               'Action' : 'PUT' 
           },
           'director': {
               'Value'  : data['director'],
               'Action' : 'PUT'
           }
       },
 
       ReturnValues = "UPDATED_NEW"  # returns the new updated values
   )
   return response

# def update_in_movie(id, data:dict):
#     print(data)
#     key_id = data['id']
#     print(key_id)
#     if id == key_id:
#         response = MovieTable.update_item(
#            Key = {
#                'id': int(id)
#             },
#             AttributeUpdates={
#                'title': {
#                    'Value'  : data['title'],
#                    'Action' : 'PUT' 
#                 },
#                'director': {
#                    'Value'  : data['director'],
#                    'Action' : 'PUT'
#                }
#             },
 
#             ReturnValues = "UPDATED_NEW"  # returns the new updated values
#         )
#         return response
#     return {
#     'msg'       : 'record not present in table'
#    } 

#function for delete item from table
def delete_from_movie(id):
    response = MovieTable.delete_item(
        Key = {
            'id': int(id)
        }
    )
    return response

app = Flask(__name__) 
@app.route('/')
def root_route():
   print("Hello World!") 
#    app.run(host="localhost", port=5050, debug=True)
   dynamodb.create_table_movie()
   return 'Table created'
 
@app.route('/getmovie/<id>', methods=['GET'])
def get_movie(id):
   print(id)
   response = dynamodb.read_from_movie(id)
   if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
       if ('Item' in response):
           return { 'Item': response['Item'] }
       return { 'msg' : 'Item not found!' }
   return {
       'msg': 'error occurred',
       'response': response
   }

# @app.route('/movie', methods=['POST'])
# def add_movie():
#    data = request.get_json()
#    print(data)
#    response = dynamodb.write_to_movie(data['id'], data['title'], data['director'])   
#    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
#        return {
#            'msg': 'Add Movie successful',
#        }
#    return { 
#        'msg': 'error occurred',
#        'response': response
#    }
@app.route('/movie', methods=['GET','POST'])
def add_movie():
#    print(data)
#    response = dynamodb.write_to_movie(data['id'], data['title'], data['director'])   
    data = request.get_json()
    key_id = data['id']
    response = dynamodb.read_from_movie(key_id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        if ('Item' in response):
            return{
                'msg': 'Item with same ID already present'
            }
        data = request.get_json()
        response = dynamodb.write_to_movie(data['id'], data['title'], data['director'])  
        return {
           'msg': 'Add Movie successful'
        }
    return { 
       'msg': 'error occurred',
       'response': response
   }

@app.route('/updatemovie/<id>', methods=['GET','PUT'])
def update_movie(id):
    # data = request.get_json()
    # response = dynamodb.update_in_movie(id, data)
    response = dynamodb.read_from_movie(id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        if ('Item' in response):
            data = request.get_json()
            response = dynamodb.update_in_movie(id, data)
            return {
                'msg' : 'update successful'
            }
            # return { 'Item': response['Item'] }
        return { 'msg' : 'Item not found!' }
    return {
           'msg'                : 'update successful',
           'response'           : response['ResponseMetadata'],
           'ModifiedAttributes' : response['Attributes']
        }
    # return {
    #     'msg'      : 'error occurred',
    #        'response' : response
    # } 


# @app.route('/updatemovie/<id>', methods=['GET','PUT'])
# def update_movie(id):
#     data = request.get_json()
#     response = dynamodb.update_in_movie(id, data)
#     if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
#         return {
#            'msg'                : 'update successful',
#            'response'           : response['ResponseMetadata'],
#            'ModifiedAttributes' : response['Attributes']
#         }
#     return {
#         'msg'      : 'error occurred',
#            'response' : response
#    } 

@app.route('/deletemovie/<int:id>', methods=['DELETE'])
def delete_movie(id):
    response = dynamodb.read_from_movie(id)
    # response = dynamodb.delete_from_movie(id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        if ('Item' in response):
            response = dynamodb.delete_from_movie(id)
            return {
                'msg' : 'Deleted successfully'
            }
        return { 'msg' : 'Item not found!' }
    return {  
        'msg': 'Some error occcured',
        'response': response
    } 

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5051, debug=True)

def handler(event, context):
	print("hello from lambda")
	return serverless_wsgi.handle_request(app, event, context)
