from tkinter import *
from tkinter import ttk
from analysis import views_by_country, views_by_continent, top_readers
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

file_path = "./data/issuu_sample.json"

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

ttk.Label(frame_main, text="Enter document UUID:").pack()
ttk.Entry(frame_main, textvariable=doc_input, width=60).pack()

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
ttk.Button(btn_frame, text="Top 10 Readers", command=show_top_readers).grid(row=0, column=2, padx=5)

# HISTOGRAM DISPLAY FRAME
frame_histogram = ttk.Frame(root, padding="10")
frame_histogram.pack(fill=BOTH, expand=True)

root.mainloop()
