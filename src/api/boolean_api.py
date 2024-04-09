import json
from flask import Blueprint, request, jsonify, Response
import nltk
from information_retrieval.boolean_model import search_boolean_model
from db.posts import get_all_posts
from marshmallow import Schema, fields

boolean_search_blueprint = Blueprint('boolean_search', __name__)
# Boolean Model endpoint
# http://127.0.0.1:5000/search/boolean
@boolean_search_blueprint.route('/search/boolean', methods=['POST'])
async def search_post():
    json_request = request.get_json()
    
    operator_value_list = []
    lemmatizer = nltk.stem.WordNetLemmatizer()
 
    for item in json_request:
        word = lemmatizer.lemmatize(item['value'].lower())
        operator_value_list.append((item['operator'], word.lower()))
    
    id_list = search_boolean_model(operator_value_list)
    
    posts = await get_all_posts()
    print(len(posts))
    filtered_posts = [post for post in posts if post.id in id_list]
        
    object_schema = ObjectSchema()
    json_string = object_schema.dumps(filtered_posts, many=True)
    
    return json_string
    
class ObjectSchema(Schema):
    id = fields.Str()
    title = fields.Str()
    content = fields.Str()
    published_on = fields.Str()
    link = fields.Str()
    source = fields.Str()

