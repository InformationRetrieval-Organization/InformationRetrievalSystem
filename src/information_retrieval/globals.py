def init():
    """
    Initialize the global variables
    """
    global _inverted_index
    global _term_frequency
    global _all_doc_ids
    global _term_document_weight_matrix
    global _document_id_vector_map
    global _vocabulary
    global _date_coefficient
    
    _inverted_index = {} # Store Posting Lists in a dictionary with the word as the key and the value as a list of post_ids
    _term_frequency = {} # Store the term frequency of each word
    _all_doc_ids = set() # Store all the document ids
    _term_document_weight_matrix = [] # Is a two dimensional array with n Documentvectors
    _document_id_vector_map= {} # Map each Documentid to the correct Vector
    _vocabulary = [] # List of str
    _date_coefficient = {} # Store the date coefficient for each document
    
    