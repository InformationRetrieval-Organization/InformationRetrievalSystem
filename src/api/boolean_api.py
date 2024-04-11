from flask import Blueprint, request
import nltk
from src.information_retrieval.boolean_model import search_boolean_model
from src.db.posts import get_all_posts
from src.api.schemas import ObjectSchema
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
    
    id_list = search_boolean_model(operator_value_list)
    
    posts = await get_all_posts()
    filtered_posts = [post for post in posts if post.id in id_list]
    
    # Sort posts based on time
    filtered_posts.sort(key=lambda x: x.published_on, reverse=True)
    
    object_schema = ObjectSchema()
    json_string = object_schema.dumps(filtered_posts, many=True)
    
    return json_string


