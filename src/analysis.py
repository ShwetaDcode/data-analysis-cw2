from dataloader import load_data
from collections import defaultdict
from continents import continent_map
import matplotlib.pyplot as plt
import re
import networkx as nx

def views_by_country(doc_id, file_path):
    country_counter = {}

    for record in load_data(file_path):
        if record.get("subject_doc_id") == doc_id:
            country = record.get("visitor_country")
            if country:
                country_counter[country] = country_counter.get(country, 0) + 1

    return country_counter



def views_by_continent(doc_id, file_path):
    result = views_by_country(doc_id, file_path)
    continent_counter = {}

    for country, count in result.items():
        continent = None
        for cont, countries in continent_map.items():
            if country in countries:
                continent = cont
                break

        if not continent:
            continent = "Unknown"

        continent_counter[continent] = continent_counter.get(continent, 0) + count

    return continent_counter


def views_by_browser_full(file_path):
    browser_counter = {}
    for record in load_data(file_path):
        user_agent = record.get("visitor_useragent")
        if user_agent:
            browser_counter[user_agent] = browser_counter.get(user_agent, 0) + 1
    return browser_counter

def extract_main_browser(user_agent):
    if not user_agent:
        return "Unknown"

    browsers = ["Firefox", "Chrome", "Safari", "Opera", "Edge", "IE", "Mozilla"]

    for browser in browsers:
        match = re.search(fr'{re.escape(browser)}[/ ]\d+', user_agent, re.IGNORECASE)
        if match:
            return browser
        
    return "Other"

def views_by_browser_main(file_path):
    browser_counter = {}
    
    full_agents_counts = views_by_browser_full(file_path)

    for user_agent, count in full_agents_counts.items():
        main_browser = extract_main_browser(user_agent)
        browser_counter[main_browser] = browser_counter.get(main_browser, 0) + count
        
    return browser_counter


def top_readers(file_path, limit=10):

    readers = {}

    for record in load_data(file_path):
        if record.get("event_type") == "pagereadtime":
            user = record.get("visitor_uuid")
            read_time = record.get("event_readtime", 0)

            if user:
                readers[user] = readers.get(user, 0) + read_time

    sorted_readers = sorted(readers.items(), key=lambda x: x[1], reverse=True)

    return sorted_readers[:limit]

# --- Task 5: "Also Likes" functionality ---

def readers_of_document(doc_id, file_path):
    """
    Task 5a: Returns a set of all visitor UUIDs that have viewed a given document ID.
    Looks for the document in both subject_doc_id and env_doc_id.
    """
    reader_uuids = set()
    for record in load_data(file_path):
        # Check if the event is related to the target document
        if record.get("subject_doc_id") == doc_id or record.get("env_doc_id") == doc_id:
            visitor_uuid = record.get("visitor_uuid")
            if visitor_uuid:
                reader_uuids.add(visitor_uuid)
    return reader_uuids


def documents_read_by_visitor(visitor_uuid, file_path):
    """
    Task 5b: Returns a set of all document UUIDs read by a given visitor UUID.
    Includes documents found in subject_doc_id and env_doc_id.
    """
    doc_uuids = set()
    for record in load_data(file_path):
        if record.get("visitor_uuid") == visitor_uuid:
            # Look at documents being acted upon (subject)
            subject_doc = record.get("subject_doc_id")
            if subject_doc:
                doc_uuids.add(subject_doc)
            
            # Look at the document context (environment)
            env_doc = record.get("env_doc_id")
            if env_doc:
                doc_uuids.add(env_doc)
    return doc_uuids


def also_likes_documents(doc_id, file_path, sort_func, visitor_uuid_filter=None):
    """
    Task 5c: Implements the "also likes" functionality, parametrised by a sorting function.

    Parameters:
    - doc_id (str): The primary document UUID.
    - file_path (str): Path to the data file.
    - sort_func (function): A function that takes (document_uuid, shared_reader_count) 
      and returns a sort key (score).
    - visitor_uuid_filter (str, optional): If provided, only documents read by this 
      specific visitor (and only if they also read doc_id) are considered.

    Returns:
    - list of tuples: [(document_uuid, sort_score), ...] sorted by the sort score (descending).
    """
    readers = readers_of_document(doc_id, file_path)
    
    if visitor_uuid_filter:
        if visitor_uuid_filter in readers:
            readers = {visitor_uuid_filter}
        else:
            return []

    also_liked_counts = defaultdict(int)

    for reader_id in readers:
        docs_read = documents_read_by_visitor(reader_id, file_path)
        for other_doc_id in docs_read:
            if other_doc_id != doc_id:
                also_liked_counts[other_doc_id] += 1
    
    scored_documents = []
    for other_doc_id, count in also_liked_counts.items():
        score = sort_func(other_doc_id, count)
        scored_documents.append((other_doc_id, score))

    sorted_list = sorted(scored_documents, key=lambda item: item[1], reverse=True)
    
    return sorted_list


def sort_by_shared_readers(doc_id, shared_reader_count):

    return shared_reader_count


def also_likes_task_5d(doc_id, visitor_uuid, file_path):

    sorted_list = also_likes_documents(
        doc_id=doc_id, 
        file_path=file_path, 
        sort_func=sort_by_shared_readers, 
        visitor_uuid_filter=visitor_uuid
    )
    
    return sorted_list[:10]


# ----------------------------------------------------------------------------------

# --- Task 6: Also Likes Graph ---

def generate_also_likes_graph(doc_id, visitor_uuid, file_path, top_n=10):
    """
    Task 6: Generates a NetworkX graph based on the "also likes" relationship.
    
    The graph includes the primary document and the top_n related documents,
    with edge weights representing the number of shared readers.
    
    Returns: A networkx.Graph object.
    """

    sorted_likes = also_likes_documents(
        doc_id=doc_id, 
        file_path=file_path, 
        sort_func=sort_by_shared_readers, 
        visitor_uuid_filter=visitor_uuid
    )
    
    top_likes = sorted_likes[:top_n]
    
    G = nx.Graph()
    
    G.add_node(doc_id, label=doc_id[:8] + '...', type='Primary')
    
    for liked_doc_id, shared_readers in top_likes:
        G.add_node(liked_doc_id, label=liked_doc_id[:8] + '...', type='Secondary')
        G.add_edge(doc_id, liked_doc_id, weight=shared_readers)
        
    return G

# ----------------------------------------------------------------------------------

def show_histogram(data_dict, title):
    plt.bar(range(len(data_dict)), list(data_dict.values()))
    plt.xticks(range(len(data_dict)), list(data_dict.keys()))
    plt.title(title)
    plt.show()
