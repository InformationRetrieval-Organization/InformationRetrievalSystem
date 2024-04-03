from flask import Flask
from api.vector_space_api import vector_space_search_blueprint
from api.boolean_api import boolean_search_blueprint
from data_crawlers.nyt_data_crawler import crawl_nyt_data

app = Flask(__name__)
app.register_blueprint(vector_space_search_blueprint)
app.register_blueprint(boolean_search_blueprint)

if __name__ == "__main__":
    # Crawl data from New York Times and store in database
    #crawl_nyt_data()

    # Run the Flask app
    app.run(debug=True)