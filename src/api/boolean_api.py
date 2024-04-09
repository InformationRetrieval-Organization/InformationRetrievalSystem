from flask import Blueprint, request
import nltk

from information_retrieval.boolean_model import search_boolean_model

boolean_search_blueprint = Blueprint('boolean_search', __name__)

# Boolean Model endpoint
# http://127.0.0.1:5000/search/boolean
@boolean_search_blueprint.route('/search/boolean', methods=['POST'])
def search_post():
    json = request.get_json()
    
    operator_value_list = []
    lemmatizer = nltk.stem.WordNetLemmatizer()
 
    for item in json:
        word = lemmatizer.lemmatize(item['value'].lower())
        operator_value_list.append((item['operator'], word.lower))
        
    return search_boolean_model(operator_value_list)
