from flask import Flask
from api.vector_space_api import vector_space_search_blueprint
from api.boolean_api import boolean_search_blueprint
from data_crawlers.nyt_data_crawler import crawl_nyt_data
from information_retrieval.vector_space_model import build_vector_space_model
from information_retrieval.boolean_model import build_boolean_model

app = Flask(__name__)
app.register_blueprint(vector_space_search_blueprint)
app.register_blueprint(boolean_search_blueprint)

if __name__ == "__main__":
    # Crawl data from New York Times and store in database
    crawl_nyt_data()

    #Todo: Preprocessing, steamming, stop words removal, etc.
    
    # Build Boolean model
    build_boolean_model()
    
    # Build the vector space model
    build_vector_space_model()

    # Run the Flask app
    app.run(debug=True)