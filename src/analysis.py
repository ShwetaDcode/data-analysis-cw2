from dataloader import load_data
from collections import defaultdict
from continents import continent_map
import matplotlib.pyplot as plt
import re

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


def top_readers(file_path, limit=10):
    """Return the top readers sorted by total reading time."""
    readers = {}

    for record in load_data(file_path):
        # Only consider records that include reading time
        if record.get("event_type") == "pagereadtime":
            user = record.get("visitor_uuid")
            read_time = record.get("event_readtime", 0)

            if user:
                readers[user] = readers.get(user, 0) + read_time

    # Sort by total time spent reading (descending order)
    sorted_readers = sorted(readers.items(), key=lambda x: x[1], reverse=True)

    return sorted_readers[:limit]

def show_histogram(data_dict, title):
    plt.bar(range(len(data_dict)), list(data_dict.values()))
    plt.xticks(range(len(data_dict)), list(data_dict.keys()))
    plt.title(title)
    plt.show()
