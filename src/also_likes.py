# also_likes.py
from dataloader import load_data
import networkx as nx

READ_EVENTS = {"read", "pageread", "pagereadtime"}

# FUNCTION A — Readers of a given document
def get_readers_for_doc(doc_id, file_path):
    readers = set()

    for record in load_data(file_path):
        if record.get("subject_doc_id") == doc_id:
            if record.get("event_type") in READ_EVENTS:
                uuid = record.get("visitor_uuid")
                if uuid:
                    readers.add(uuid)

    return readers



# FUNCTION B — Docs read by a given reader
def get_docs_for_reader(visitor_uuid, file_path):
    docs = set()

    for record in load_data(file_path):
        if record.get("visitor_uuid") == visitor_uuid:
            if record.get("event_type") in READ_EVENTS:
                doc_id = record.get("subject_doc_id")
                if doc_id:
                    docs.add(doc_id)

    return docs



# FUNCTION C — Also Likes Core Logic

def also_likes(doc_id, file_path, sort_fn, limit=10):
    '''
    ill print it with all the steps to get to the final result
    '''
    # 1. Get all readers of this document
    readers = get_readers_for_doc(doc_id, file_path)
    print(f"Readers who viewed this document ({len(readers)} total):")
    print(readers)

    # 2. Count other documents read by those readers and the doc id
    like_counter = {}
    for reader in readers:
        docs = get_docs_for_reader(reader, file_path)
        print(f"\nReader {reader} read these documents:")
        print(docs)
        for d in docs:
            # Don't count the original document itself
            if d != doc_id:
                like_counter[d] = like_counter.get(d, 0) + 1
    # 3. Sort using the function that is passed in
    sorted_docs = sort_fn(like_counter)
    top_n = sorted_docs[:limit]
    print(f"\nFUNCTION D: Top {limit} 'also liked' documents:")
    if not top_n:
        print("No 'also liked' documents found.")
    else:
        for doc, count in top_n:
            print(f"{doc}  =>  {count} shared readers")

    return top_n


# Example: default sorting function
def sort_by_reader_count(doc_dict):
    """
    Sorts documents by the number of readers (descending)
    item = (doc_id, count)
    """
    return sorted(doc_dict.items(), key=lambda x: x[1], reverse=True)

# FUNCTION D  (asks user for new input)
def function_d_run(doc_id, visitor_uuid, file_path):
    print("\nInput document:", doc_id)
    print("Input visitor:", visitor_uuid)

    result = also_likes(doc_id, file_path, sort_by_reader_count)
    return result


def generate_also_likes_graph(doc_id, visitor_uuid, file_path, top_n=10):
    """
    Builds a directed graph using your also_likes() output.
    Uses last 4 characters for labels (CW requirement).
    """

    # Get top also-liked docs using YOUR function C + sorting
    top_likes = also_likes(doc_id, file_path, sort_by_reader_count, limit=top_n)

    G = nx.DiGraph()

    # Add main document node
    G.add_node(doc_id, label=doc_id[-4:], type="PrimaryDoc")

    # Optionally add main visitor node
    if visitor_uuid:
        G.add_node(visitor_uuid, label=visitor_uuid[-4:], type="PrimaryUser")
        G.add_edge(visitor_uuid, doc_id)  # user -> document

    # Add also-liked documents
    for liked_doc, count in top_likes:
        G.add_node(liked_doc, label=liked_doc[-4:], type="SecondaryDoc")

        # Connect related doc to main doc
        G.add_edge(doc_id, liked_doc, weight=count)

        # Add linking readers
        readers = get_readers_for_doc(liked_doc, file_path)

        for r in readers:
            short_user = r[-4:]
            G.add_node(r, label=short_user, type="Reader")
            G.add_edge(r, liked_doc)

    return G
#testing from terminal

if __name__ == "__main__":
    test_file = "data/issuu_sample.json"
    test_doc = "140219141540-c900b41f845c67cc08b58911155c681c"
    visitor = "af2d901db71d1795"

    print("\nFUNCTION A: Readers of this document")
    readers = get_readers_for_doc(test_doc, test_file)
    print(f"Readers of this document: {test_doc}:")
    print(readers)

    print("\nFUNCTION B: Docs read by a reader")
    docs = get_docs_for_reader(visitor, test_file)
    print(f"Reader {visitor} read: {docs}")

# FUNCTION C
    also_likes(test_doc, test_file, sort_by_reader_count)
    #function D input
    doc_id = input("Enter document UUID: ")
    visitor_uuid = input("Enter visitor UUID: ")
    # FUNCTION D (user input)
    function_d_run(doc_id, visitor_uuid, test_file)