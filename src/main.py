import argparse
import subprocess
import os
import sys
import networkx as nx

from analysis import (
    views_by_country, 
    views_by_continent, 
    views_by_browser_full, 
    views_by_browser_main, 
    top_readers,
    also_likes_task_5d, 
    generate_also_likes_graph 
)

def launch_gui():
    gui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gui.py')
    
    print("Launching GUI application (Task 7)...")
    try:
        subprocess.run([sys.executable, gui_path])
    except FileNotFoundError:
        print(f"Error: Could not find Python interpreter at {sys.executable}.")
    except Exception as e:
        print(f"An error occurred while launching the GUI: {e}")


def run_cli_task(task_id, file_name, doc_uuid=None, user_uuid=None):
    print(f"\n--- Running Task {task_id} with file: {file_name} ---")
    
    result = None
    
    task_map = {
        '2a': (views_by_country, "Views by Country (requires doc_uuid)"),
        '2b': (views_by_continent, "Views by Continent (requires doc_uuid)"),
        '3a': (views_by_browser_full, "Views by Full Browser User Agent"),
        '3b': (views_by_browser_main, "Views by Main Browser Name"),
        '4': (top_readers, "Top 10 Readers (Total Reading Time)"),
        '5d': (also_likes_task_5d, "Also Likes - Top 10 Documents by Shared Readers"),
        '6': (generate_also_likes_graph, "Also Likes Graph Generation (requires doc_uuid)"), # Updated Task 6
    }

    if task_id == '7':
        launch_gui()
        return

    if task_id not in task_map:
        print(f"Error: Invalid task ID '{task_id}'. Valid IDs are: {', '.join(task_map.keys())} and '7'.")
        return

    func, description = task_map[task_id]

    try:
        if task_id in ['2a', '2b']:
            if not doc_uuid:
                print(f"Error: Task {task_id} requires a document UUID (-d argument).")
                return
            result = func(doc_uuid, file_name)

        elif task_id == '5d':
            if not doc_uuid:
                print(f"Error: Task {task_id} requires a document UUID (-d). User UUID (-u) is optional.")
                return
            result = func(doc_uuid, user_uuid, file_name)
        
        elif task_id == '6':
            if not doc_uuid:
                print(f"Error: Task {task_id} requires document UUID (-d). User UUID (-u) is optional.")
                return
            result = func(doc_uuid, user_uuid, file_name)

        elif task_id in ['3a', '3b', '4']:
            result = func(file_name)
        
        
        print(f"Task: {description}")
        print("-" * len(description))
        
        if isinstance(result, dict):
            sorted_result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
            for key, value in sorted_result.items():
                print(f"{key}: {value}")
        elif isinstance(result, list):
            if task_id == '4':
                print("Top Readers (UUID → Time in Seconds):")
                for user, time in result:
                    print(f"{user} → {time} seconds")
            elif task_id == '5d':
                filter_status = f"readers of {doc_uuid}" if user_uuid is None else f"reader {user_uuid}"
                print(f"Top 10 Documents also liked by {filter_status} (Shared Readers → Document UUID):")                
                for doc, score in result:
                    print(f"{int(score)} → {doc}")
            else:
                print(result) 

        elif isinstance(result, nx.Graph):
            print(f"Also Likes Graph generated successfully for document {doc_uuid}.")
            if result.number_of_edges() > 0:
                print(f"Graph details: {result.number_of_nodes()} documents, {result.number_of_edges()} connections.")
                print("\nTop Connections (Weight is Shared Readers Count):")
                for u, v, data in result.edges(data=True):
                    print(f"  {u[:8]}... --({data['weight']})--> {v[:8]}...")
            else:
                print("No 'Also Likes' connections found for this document/filter.")
        
        else:
            print(result)

    except FileNotFoundError:
        print(f"Error: Input file '{file_name}' not found. Please check the path and file name.")
    except Exception as e:
        print(f"An unexpected error occurred during task execution: {e}")


def main():
    
    parser = argparse.ArgumentParser(
        description="Run analytics tasks on document tracker data.",
        usage='%(prog)s -f <file_name> -t <task_id> [-d <doc_uuid>] [-u <user_uuid>]'
    )
    
    parser.add_argument('-u', '--user_uuid', default=None, help="Visitor UUID (Required for later tasks like 5, 6).")
    parser.add_argument('-d', '--doc_uuid', default=None, help="Document UUID (Required for tasks 2a, 2b).")
    parser.add_argument('-t', '--task_id', required=True, 
                        choices=['2a', '2b', '3a', '3b', '4', '5d', '6', '7'],
                        help="Task ID to execute (e.g., 2a, 3b, 7).")
    parser.add_argument('-f', '--file_name', required=True, help="Name of the JSON input file (e.g., data/issuu_sample.json).")

    args = parser.parse_args()
    
    run_cli_task(args.task_id, args.file_name, args.doc_uuid, args.user_uuid)


if __name__ == "__main__":
    main()