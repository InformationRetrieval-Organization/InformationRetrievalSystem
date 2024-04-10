import requests
import json
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

base_url = "http://127.0.0.1:5000"
boolean_api_url = f"{base_url}/search/boolean"
vector_space_url = f"{base_url}/search/vector-space"

queries = ["korea", "election", "korea election", "president", "parties"]


def calculate_recall_precision(relevant_docs, retrieved_docs):
    """
    Calculate recall and precision
    TODO: mark the relevant documents in the retrieved documents manually
    https://github.com/InformationRetrieval-Organization/InformationRetrievalSystem/issues/8
    """
    relevant_retrieved_docs = set(relevant_docs).intersection(set(retrieved_docs))

    recall = len(relevant_retrieved_docs) / len(relevant_docs) if relevant_docs else 0
    precision = (
        len(relevant_retrieved_docs) / len(retrieved_docs) if retrieved_docs else 0
    )

    return recall, precision


def call_boolean_api(query):
    """
    Call Boolean API
    """
    url = f"{boolean_api_url}"
    body = [{"operator": "AND", "value": word} for word in query.split()]
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    response.raise_for_status()

    return response.json()


def call_vector_space_api(query):
    """
    Call Vector Space API
    """
    query_string = "+".join(query.split())
    url = f"{vector_space_url}?q={query_string}"
    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def calculate_temporal_relevance(retrieved_docs):
    """
    Calculate temporal relevance
    """
    if not retrieved_docs:
        return None

    current_date = datetime.now()

    # get all publication dates
    publication_dates = [
        datetime.strptime(doc["published_on"], "%Y-%m-%d %H:%M:%S%z")
        for doc in retrieved_docs
    ]

    # calculate average publication date
    average_publication_date = sum(
        (
            pub_date - datetime(1970, 1, 1, tzinfo=timezone.utc)
            for pub_date in publication_dates
        ),
        timedelta(0),
    ) / len(publication_dates)

    difference_in_days = (current_date - average_publication_date).day

    return difference_in_days


if __name__ == "__main__":
    """
    Evaluate Boolean and Vector Space Models
    """
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
