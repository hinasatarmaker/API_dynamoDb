from boto3 import resource
import config

AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
REGION_NAME = config.REGION_NAME
 
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