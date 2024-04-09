def init():
    global _inverted_index
    global _term_frequency
    global _all_doc_ids

    _inverted_index = {} # Store Posting Lists in a dictionary with the word as the key and the value as a list of post_ids
    _term_frequency = {} # Store the term frequency of each word
    _all_doc_ids = set() # Store all the document ids