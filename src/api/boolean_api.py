from flask import Blueprint, request

from information_retrieval.boolean_model import search_boolean_model

boolean_search_blueprint = Blueprint('boolean_search', __name__)

# Boolean Model endpoint
# http://127.0.0.1:5000/search/boolean
@boolean_search_blueprint.route('/search/boolean', methods=['POST'])
def search_post():
    json = request.get_json()
    
    operator_value_list = [] 
    for item in json:
        operator_value_list.append((item['operator'], item['value'])) 
    
    return search_boolean_model(operator_value_list)
