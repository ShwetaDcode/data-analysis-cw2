from dataloader import load_data
from analysis import views_by_country, views_by_continent, show_histogram, top_readers
from also_likes import function_d_run, generate_also_likes_graph
from browser_analysis import views_by_browser_main, views_by_browser_full
import argparse

parser = argparse.ArgumentParser(description="Coursework 2 - Document Analytics")

parser.add_argument("-u", "--user", help="Visitor UUID")
parser.add_argument("-d", "--doc", help="Document UUID")
parser.add_argument("-t", "--task", help="Task ID (2a, 2b, 5d, 7, etc)")
parser.add_argument("-f", "--file", help="Path to JSON file", required=True)

args = parser.parse_args()

user_id = args.user
doc_id = args.doc
task_id = args.task
file_path = args.file

if task_id == "2a":
    # Country histogram
    country_result = views_by_country(doc_id, file_path)
    print("\nCountry views:", country_result)
    show_histogram(country_result, "Views by Country")

elif task_id == "2b":
    # Continent histogram
    continent_result = views_by_continent(doc_id, file_path)
    print("\nContinent views:", continent_result)
    show_histogram(continent_result, "Views by Continent")

elif task_id == "3a":
        # Full browser strings
    browser_result = views_by_browser_full(file_path)
    print("\nViews by Browser (FULL user agent):")
    show_histogram(browser_result, "Views by Browser (Full user agent)")
elif task_id == "3b":
   # Main browser only (Chrome, Firefox, etc)
    browser_result = views_by_browser_main(file_path)
    print("\nViews by Browser (MAIN browser only):")
    print(browser_result)
    show_histogram(browser_result, "Views by Browser (Main browser)")

elif task_id == "4":
    # Top 10 readers
    top10 = top_readers(file_path)
    print("\nTop 10 Readers (visitor_uuid, total_time):")
    for user, time in top10:
        print(user, "=>", time, "seconds")

elif task_id == "5d":
    # Also Likes
    also_liked_docs = function_d_run(doc_id, user_id, file_path)
    print("\nTop 10 'Also Liked' Documents:")
    print(also_liked_docs)

elif task_id == "6":
    G = generate_also_likes_graph(doc_id, user_id, file_path)

    print("\nGraph created. Nodes:")
    print(G.nodes(data=True))

    print("\nEdges:")
    print(G.edges())

elif task_id == "7":
    print("Launching GUI...")
    import gui 

else:
    print("Invalid or missing task ID. Please specify a valid task using -t.")