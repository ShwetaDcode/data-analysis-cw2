from tkinter import *
from tkinter import ttk
from analysis import views_by_country, views_by_continent, top_readers, views_by_browser_full, views_by_browser_main, also_likes_task_5d, generate_also_likes_graph # Import new functions
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx

file_path = "../data/issuu_sample.json"

def show_histogram(data_dict, title):
    """Re-usable histogram embedder for Tkinter."""
    # Clear existing histogram
    for widget in frame_histogram.winfo_children():
        widget.destroy()

    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(range(len(data_dict)), list(data_dict.values()), color="skyblue")
    ax.set_xticks(range(len(data_dict)))
    ax.set_xticklabels(list(data_dict.keys()))
    ax.set_title(title)
    ax.set_ylabel("Views")

    # Embed into GUI frame
    canvas = FigureCanvasTkAgg(fig, master=frame_histogram)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)


def generate_country_hist():
    doc_id = doc_input.get()
    results = views_by_country(doc_id, file_path)
    show_histogram(results, f"Views by Country")


def generate_continent_hist():
    doc_id = doc_input.get()
    results = views_by_continent(doc_id, file_path)
    show_histogram(results, f"Views by Continent")

# ---------------------------------------------------------------------

def generate_browser_full_hist(): # Task 3a
    results = views_by_browser_full(file_path)
    show_histogram(results, f"Views by Full Browser User Agent")

def generate_browser_main_hist(): # Task 3b
    results = views_by_browser_main(file_path)
    show_histogram(results, f"Views by Main Browser Name")

def show_also_likes(): # Task 5d
    doc_id = doc_input.get()
    visitor_id = visitor_input.get().strip() or None
    
    text_display.delete(1.0, END)
    
    if not doc_id:
        text_display.insert(END, "Error: Document UUID is required for 'Also Likes' functionality.")
        return

    text_display.insert(END, "Calculating 'Also Likes'...\n")
    
    try:
        results = also_likes_task_5d(doc_id, visitor_id, file_path)
        
        if visitor_id:
            text_display.insert(END, f"Results for readers of DOC ID {doc_id[:10]}... who are VISITOR {visitor_id[:10]}...:\n\n")
        else:
            text_display.insert(END, f"Results for ALL readers of DOC ID {doc_id[:10]}...:\n\n")

        if not results:
            text_display.insert(END, "No 'Also Likes' documents found based on the inputs.")
            return

        text_display.insert(END, "Top 10 Also Likes (Shared Readers → Document UUID):\n")
        text_display.insert(END, "-------------------------------------------------------\n")
        
        for idx, (doc, score) in enumerate(results, start=1):
            text_display.insert(END, f"{idx}. {int(score)} readers → {doc}\n")
            
    except Exception as e:
        text_display.insert(END, f"An error occurred: {e}")


def show_also_likes_graph(): # Task 6
    doc_id = doc_input.get()
    visitor_id = visitor_input.get() or None
    
    text_display.delete(1.0, END)
    for widget in frame_histogram.winfo_children():
        widget.destroy()
    
    if not doc_id:
        text_display.insert(END, "Error: Document UUID is required to generate the Also Likes graph.")
        return

    text_display.insert(END, f"Generating 'Also Likes' Graph for document {doc_id[:10]}... \n")
    if visitor_id:
        text_display.insert(END, f"Filtered by visitor: {visitor_id[:10]}...\n")
    
    try:
        G = generate_also_likes_graph(doc_id, visitor_id, file_path, top_n=10)
        
        if not G.edges:
            text_display.insert(END, "No related documents found to form a graph.")
            return

        fig, ax = plt.subplots(figsize=(6, 4))
        
        pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42) 
        
        node_colors = ['#FF6347' if G.nodes[n]['type'] == 'Primary' else '#4682B4' for n in G.nodes()]
        
        edge_weights = [G.get_edge_data(u, v)['weight'] for u, v in G.edges()]
        max_weight = max(edge_weights)
        edge_widths = [1 + 7 * (w / max_weight) for w in edge_weights]

        nx.draw_networkx_nodes(G, pos, 
                               node_color=node_colors, 
                               node_size=1500, 
                               alpha=0.8,
                               ax=ax)

        nx.draw_networkx_edges(G, pos, 
                               width=edge_widths, 
                               edge_color="gray", 
                               alpha=0.6, 
                               ax=ax)

        labels = {n: G.nodes[n]['label'] for n in G.nodes()}
        nx.draw_networkx_labels(G, pos, 
                                labels=labels, 
                                font_size=8, 
                                font_color="black", 
                                ax=ax)
        
        title = f"Also Likes Graph for Document {doc_id[:10]}..."
        if visitor_id:
            title += f"\n(Filtered by Reader {visitor_id[:10]}...)"
            
        ax.set_title(title, fontsize=10)
        ax.axis('off') 
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame_histogram)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        text_display.insert(END, "Graph generated successfully.\n")

    except Exception as e:
        text_display.insert(END, f"An error occurred during graph generation: {e}")  

# ---------------------------------------------------------------------

def show_top_readers():
    text_display.delete(1.0, END)  # Clear previous text    
    results = top_readers(file_path)
    text_display.insert(END, "Top 10 Readers MOST time spent :\n\n")
    for idx, (user, time) in enumerate(results, start=1):
        text_display.insert(END, f"{idx}. {user} → {time} seconds\n")

root = Tk()
root.title("Document Tracker Analytics - Histogram Viewer")

# MAIN INPUT FRAME
frame_main = ttk.Frame(root, padding="10")
frame_main.pack(fill=BOTH)

doc_input = StringVar()
visitor_input = StringVar() 

ttk.Label(frame_main, text="Document UUID (-d):").grid(row=0, column=0, sticky=W, padx=5, pady=2)
ttk.Entry(frame_main, textvariable=doc_input, width=60).grid(row=0, column=1, columnspan=4, padx=5, pady=2, sticky=EW)

ttk.Label(frame_main, text="Visitor UUID (-u) [Optional]:").grid(row=1, column=0, sticky=W, padx=5, pady=2)
ttk.Entry(frame_main, textvariable=visitor_input, width=60).grid(row=1, column=1, columnspan=4, padx=5, pady=2, sticky=EW)

# LEFT PANEL (Top readers printout)
frame_left = ttk.Frame(root, padding="10")
frame_left.pack(side=LEFT, fill=Y)

Label(frame_left, text="Analytics Output").pack()
text_display = Text(frame_left, width=40, height=40)
text_display.pack(fill=Y)

# BUTTONS
btn_frame = ttk.Frame(frame_main)
btn_frame.grid(row=2, column=0, columnspan=5, pady=10)

# Task 2a, 2b, 4
ttk.Button(btn_frame, text="Views by Country (2a)", command=generate_country_hist).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(btn_frame, text="Views by Continent (2b)", command=generate_continent_hist).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(btn_frame, text="Top 10 Readers (4)", command=show_top_readers).grid(row=0, column=2, padx=5, pady=5)

# Task 3a, 3b
ttk.Button(btn_frame, text="Browser (Full Agent 3a)", command=generate_browser_full_hist).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(btn_frame, text="Browser (Main Name 3b)", command=generate_browser_main_hist).grid(row=1, column=1, padx=5, pady=5)

# Task 5d and 6
ttk.Button(btn_frame, text="Also Likes (5d)", command=show_also_likes).grid(row=1, column=2, padx=5, pady=5)
ttk.Button(btn_frame, text="Also Likes Graph (6)", command=show_also_likes_graph).grid(row=2, column=1, padx=5, pady=5) # New button for Task 6

# HISTOGRAM DISPLAY FRAME
frame_histogram = ttk.Frame(root, padding="10")
frame_histogram.pack(fill=BOTH, expand=True)

root.mainloop()
