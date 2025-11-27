from tkinter import *
from tkinter import ttk
from analysis import views_by_country, views_by_continent, top_readers
from also_likes import function_d_run, generate_also_likes_graph
from browser_analysis import views_by_browser_full_plot_friendly, views_by_browser_full, views_by_browser_main
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx

# Small Datasets
file_path = "./data/issuu_sample.json"
# file_path = "./data/sample_tiny.json"          # Uncomment to Load
# file_path = "./data/sample_small.json"         # Uncomment to Load

# Large Datasets (Currently Only 100k lines dataset is included in zip, to maintain convenient project .zip size)
# file_path = "./data/sample_100k_lines.json"
# file_path = "./data/sample_400k_lines-1.json"  # Uncomment to Load (Not Included in .zip to maintain convenient .zip size)
# file_path = "./data/sample_600k_lines.json"    # Uncomment to Load (Not Included in .zip to maintain convenient .zip size)
# file_path = "./data/sample_3m_lines.json"      # Uncomment to Load (Not Included in .zip to maintain convenient .zip size)

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

def update_text_output(text_content): # FIX: Removed 'self' and uses global 'text_display'
    """Clears the output area and inserts new content."""
    text_display.delete('1.0', END) # FIX: Using global 'text_display'
    text_display.insert(END, text_content)

def generate_country_hist():
    doc_id = doc_input.get()
    if not doc_id:
        text_display.insert(END, "Invalid document ID or missing. Please enter a valid document UUID.\n")
        return
    results = views_by_country(doc_id, file_path)
    show_histogram(results, f"Views by Country")


def generate_continent_hist():
    doc_id = doc_input.get()
    if not doc_id:
        text_display.insert(END, "Invalid document ID or missing. Please enter a valid document UUID.\n")
        return
    results = views_by_continent(doc_id, file_path)
    show_histogram(results, f"Views by Continent")


def generate_browser_full_hist(): 
    results = views_by_browser_full(file_path)
    show_histogram(results, f"Views by Full Browser User Agent")


def generate_browser_full_hist_part():
    tagged_counts, tag_mapping = views_by_browser_full_plot_friendly(file_path)
    
    show_histogram(tagged_counts, "Views by Full Browser User Agent (Top 10/Tagged)")
    
    legend_text = "Legend for Plot-Friendly View (3a_part):\n\n"
    for tag, description in tag_mapping.items():
        legend_text += f"{tag:<10}: {description}\n"
        
    update_text_output(legend_text)


def generate_browser_main_hist():
    results = views_by_browser_main(file_path)
    show_histogram(results, f"Views by Main Browser Name")
    

def show_top_readers():
    text_display.delete(1.0, END)  # Clear previous text    
    results = top_readers(file_path)
    text_display.insert(END, "Top 10 Readers MOST time spent :\n\n")
    for idx, (user, time) in enumerate(results, start=1):
        text_display.insert(END, f"{idx}. {user} → {time} seconds\n")

def show_also_likes():
    """Run Task 5d (Also Likes) and show top 10 docs in the text area."""
    text_display.delete(1.0, END)  # Clear previous text

    doc_id = doc_input.get().strip()
    visitor = visitor_input.get().strip()

    if not doc_id:
        text_display.insert(END, "Please enter a document UUID.\n")
        return

    # Call your 5d function – it runs A, B, C internally and returns top 10
    results = function_d_run(doc_id, visitor, file_path)

    text_display.insert(END, f"Also-Likes for document:\n{doc_id}\n\n")
    if visitor:
        text_display.insert(END, f"(Visitor entered: {visitor})\n\n")

    if not results:
        text_display.insert(END, "No 'also liked' documents found.\n")
    else:
        text_display.insert(END, "Top 10 'Also Liked' documents:\n\n")
        for idx, (doc, count) in enumerate(results, start=1):
            text_display.insert(
                END,
                f"{idx}. {doc} → {count} shared readers\n"
            )

def show_also_likes_graph():
    doc_id = doc_input.get()
    visitor_id = visitor_input.get() or None

    text_display.delete(1.0, END)
    for widget in frame_histogram.winfo_children():
        widget.destroy()

    if not doc_id:
        text_display.insert(END, "Error: Document UUID is required.\n")
        return

    text_display.insert(END, f"Generating graph for {doc_id}\n")

    try:
        G = generate_also_likes_graph(doc_id, visitor_id, file_path, top_n=10)

        if len(G.nodes) == 0:
            text_display.insert(END, "No related documents found.\n")
            return

        fig, ax = plt.subplots(figsize=(6, 4))
        pos = nx.spring_layout(G, seed=42)

        node_colors = []
        for n in G.nodes():
            t = G.nodes[n].get("type")
            if t == "PrimaryDoc":
                node_colors.append("red")
            elif t == "PrimaryUser":
                node_colors.append("green")
            elif t == "SecondaryDoc":
                node_colors.append("blue")
            else:
                node_colors.append("gray")

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1400, ax=ax)
        nx.draw_networkx_edges(G, pos, arrows=True, ax=ax)

        labels = {n: G.nodes[n].get("label") for n in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)

        ax.set_title("Also Likes Graph")
        ax.axis("off")

        canvas = FigureCanvasTkAgg(fig, master=frame_histogram)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        text_display.insert(END, "Graph generated.\n")

    except Exception as e:
        text_display.insert(END, f"Error: {e}\n")

# MAIN GUI SETUP
root = Tk()
root.title("Document Tracker Analytics - Histogram Viewer")

# MAIN INPUT FRAME
frame_main = ttk.Frame(root, padding="10")
frame_main.pack(fill=BOTH)

doc_input = StringVar()
visitor_input = StringVar()

ttk.Label(frame_main, text="Enter document UUID:").pack()
ttk.Entry(frame_main, textvariable=doc_input, width=60).pack()
ttk.Label(frame_main, text="Enter visitor UUID:").pack()
ttk.Entry(frame_main, textvariable=visitor_input, width=60).pack()

# LEFT PANEL (Top readers printout)
frame_left = ttk.Frame(root, padding="10")
frame_left.pack(side=LEFT, fill=Y)

Label(frame_left, text="Analytics Output").pack()
text_display = Text(frame_left, width=40, height=40)
text_display.pack(fill=Y)

# BUTTONS
btn_frame = ttk.Frame(frame_main)
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Views by Country", command=generate_country_hist).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Views by Continent", command=generate_continent_hist).grid(row=0, column=1, padx=5)

ttk.Button(btn_frame, text="Browser (Full Agent 3a)", command=generate_browser_full_hist).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(btn_frame, text="Browser (Full Agent 3a_part)", command=generate_browser_full_hist_part).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(btn_frame, text="Browser (Main Name 3b)", command=generate_browser_main_hist).grid(row=1, column=2, padx=5, pady=5)

ttk.Button(btn_frame, text="Top 10 Readers", command=show_top_readers).grid(row=2, column=0, padx=5)

ttk.Button(btn_frame, text="Also Likes (Top 10 Docs)", command=show_also_likes).grid(row=3, column=0, padx=5)


ttk.Button(
    btn_frame,
    text="Also Likes Graph (Task 6)",
    command=show_also_likes_graph
).grid(row=3, column=1, padx=5)

# HISTOGRAM DISPLAY FRAME
frame_histogram = ttk.Frame(root, padding="10")
frame_histogram.pack(fill=BOTH, expand=True)

root.mainloop()
