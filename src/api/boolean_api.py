from flask import Blueprint, request

boolean_search_blueprint = Blueprint('boolean_search', __name__)

# Boolean Model endpoint
# http://127.0.0.1:5000/search/boolean
@boolean_search_blueprint.route('/search/boolean', methods=['POST'])
def search_post():
    json = request.get_json()
    
    dict = {} 
    for item in json:
        dict[item['operator']] = item['value']
        
    return dict