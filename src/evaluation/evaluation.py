import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

base_url = "http://127.0.0.1:5000"
boolean_api_url = f"{base_url}/search/boolean"
vector_space_url = f"{base_url}/search/vector-space"

queries = ["korea election", "president", "parties"]


def calculate_recall_precision(relevant_docs, retrieved_docs):
    relevant_retrieved_docs = set(relevant_docs).intersection(set(retrieved_docs))

    recall = len(relevant_retrieved_docs) / len(relevant_docs)
    precision = len(relevant_retrieved_docs) / len(retrieved_docs)

    return recall, precision


def call_boolean_api(query):
    url = f"{boolean_api_url}"
    body = [{"operator": "AND", "value": word} for word in query.split()]
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    response.raise_for_status()

    return response.json()


def call_vector_space_api(query):
    query_string = "+".join(query.split())
    url = f"{vector_space_url}?q={query_string}"
    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def calculate_temporal_relevance(retrieved_docs):
    current_year = datetime.now().year
    publication_years = [int(doc["published_on"].split('-')[0]) for doc in retrieved_docs]
    average_publication_year = sum(publication_years) / len(publication_years)

    return current_year - average_publication_year


if __name__ == "__main__":
    print("Evaluating Boolean and Vector Space Models")
    print("===========================================")

    results = []

    for query in queries:
        print(f"Query: {query}")

        # Call Boolean and Vector Space APIs
        boolean_api_response = call_boolean_api(query)
        vector_space_api_response = call_vector_space_api(query)

        # Get relevant and retrieved documents
        relevant_docs = [doc["id"] for doc in vector_space_api_response]
        boolean_retrieved_docs = [doc["id"] for doc in boolean_api_response]
        vector_space_retrieved_docs = [doc["id"] for doc in vector_space_api_response]

        # Calculate recall and precision
        boolean_recall, boolean_precision = calculate_recall_precision(
            relevant_docs, boolean_retrieved_docs
        )
        vector_space_recall, vector_space_precision = calculate_recall_precision(
            relevant_docs, vector_space_retrieved_docs
        )

        # Calculate temporal relevance
        boolean_temporal_relevance = calculate_temporal_relevance(boolean_api_response)
        vector_space_temporal_relevance = calculate_temporal_relevance(
            vector_space_api_response
        )

        results.append(
            {
                "query": query,
                "boolean_recall": boolean_recall,
                "boolean_precision": boolean_precision,
                "boolean_temporal_relevance": boolean_temporal_relevance,
                "vector_space_recall": vector_space_recall,
                "vector_space_precision": vector_space_precision,
                "vector_space_temporal_relevance": vector_space_temporal_relevance,
            }
        )

    df = pd.DataFrame(results)
    print(df)
    print(df.describe())

    df.set_index("query").plot(kind="bar", subplots=True, layout=(2, 3), legend=False)
    plt.tight_layout()
    plt.show()
