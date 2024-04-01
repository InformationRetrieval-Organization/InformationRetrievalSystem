from flask import Blueprint, request

search_blueprint = Blueprint('search', __name__)

# http://localhost:5000/search?q=your_search_term
@search_blueprint.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    
    return {'query': query}