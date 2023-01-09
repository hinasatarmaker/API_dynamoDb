import file1 as dynamodb
from flask import Flask
from flask import request
import serverless_wsgi

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
   print(response)
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
