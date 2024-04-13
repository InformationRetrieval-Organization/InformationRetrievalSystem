from flask import Blueprint, request
import nltk
from information_retrieval.boolean_model import search_boolean_model
from db.posts import get_all_posts
from api.schemas import ObjectSchema
from flask_cors import CORS

boolean_search_blueprint = Blueprint('boolean_search', __name__)

CORS(boolean_search_blueprint)

@boolean_search_blueprint.route('/search/boolean', methods=['POST'])
async def search_post():
    """
    Search the Boolean Model for the given query.
    url: http://127.0.0.1:5000/search/boolean
    """
    json_request = request.get_json()
    
    operator_value_list = []
    lemmatizer = nltk.stem.WordNetLemmatizer()
 
    for item in json_request:
        word = lemmatizer.lemmatize(item['value'].lower())
        operator_value_list.append((item['operator'], word.lower()))
    
    # Add synonyms to the list
    add_synonyms(operator_value_list)
    
    id_list = search_boolean_model(operator_value_list)
    
    posts = await get_all_posts()
    filtered_posts = [post for post in posts if post.id in id_list]
    
    # Sort posts based on time
    filtered_posts.sort(key=lambda x: x.published_on, reverse=True)
    
    object_schema = ObjectSchema()
    json_string = object_schema.dumps(filtered_posts, many=True)
    
    return json_string

def add_synonyms(operator_value_list):
    for item in operator_value_list:
        if item[1] == 'ppp':
            operator_value_list.add(('OR', 'people power party')) 
        elif item[1] == 'dp':
            operator_value_list.add(('OR', 'democratic party'))
        elif item[1] == 'people power party':
            operator_value_list.add(('OR', 'ppp'))
        elif item[1] == 'democratic party':
            operator_value_list.add(('OR', 'dp'))


