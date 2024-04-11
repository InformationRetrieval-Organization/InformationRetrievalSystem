import asyncio
from flask import Flask
from src.api.vector_space_api import vector_space_search_blueprint
from src.api.boolean_api import boolean_search_blueprint
from src.information_retrieval.vector_space_model import build_vector_space_model
from src.information_retrieval.boolean_model import build_boolean_model
from src.preprocessing.preprocessing import preprocess_documents
from src.db.helper import init_database
import src.information_retrieval.globals
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(vector_space_search_blueprint)
app.register_blueprint(boolean_search_blueprint)

# Enable CORS for the Flask app
CORS(app)

async def main():
    """
    Main function to run the Flask app
    """
    print("Flask app started.")

    await init_database()

    src.information_retrieval.globals.init()
    await preprocess_documents() 
    await build_boolean_model()
    await build_vector_space_model()

    app.run(host="0.0.0.0", port=8000)

# Run the main function when the script is imported
asyncio.run(main())