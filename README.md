## Document Tracker Analytics

This repository contains the source code for a data-intensive Python application designed to analyze document tracking data, such as that from the **issuu.com** platform. The application includes both a Command-Line Interface (CLI) for batch processing and a Graphical User Interface (GUI) for interactive visualization.

-----

## Getting Started

### Prerequisites

  * **Python 3.x**
  * **Required Python Libraries:**
      * `networkx`
      * `matplotlib`
      * `tkinter` (usually bundled with Python)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [repository-url]
    cd document-tracker-analytics
    ```
2.  **Install dependencies:**
    ```bash
    pip install networkx matplotlib
    ```
3.  **Data:** Ensure your JSON data file (e.g., `issuu_sample.json`) is accessible via the path used in the command-line or defined in `gui.py` (`../data/issuu_sample.json` by default).

-----

## Usage

The application can be executed in two modes: **Command-Line (CLI)** or **Graphical User Interface (GUI)**.

### 1\. Command-Line Interface (CLI)

Use `main.py` to run specific analysis tasks, which is ideal for scripting and testing.

#### Syntax

```bash
python main.py -f <file_name> -t <task_id> [-d <doc_uuid>] [-u <user_uuid>]
```

| Argument | Description | Required | Example |
| :--- | :--- | :--- | :--- |
| `-f, --file_name` | Path to the JSON input file. | **Yes** | `data/issuu_sample.json` |
| `-t, --task_id` | The analysis task to execute. | **Yes** | `2a`, `3b`, `5d`, `7` |
| `-d, --doc_uuid` | Document UUID (required for Tasks 2a, 2b, 5d, 6). | No | `1a2b3c4d5e6f` |
| `-u, --user_uuid` | Visitor UUID (optional for Tasks 5d, 6). | No | `9x8y7z6w` |

#### Available Task IDs (`-t`)

| Task ID | Description | Required Arguments |
| :--- | :--- | :--- |
| **2a** | Views by Country | `-d` |
| **2b** | Views by Continent | `-d` |
| **3a** | Views by Full Browser User Agent | None |
| **3b** | Views by Main Browser Name | None |
| **4** | Top 10 Readers (by total read time) | None |
| **5d** | Also Likes (Top 10 Documents by Shared Readers) | `-d` (and optional `-u`) |
| **6** | Also Likes Graph Generation (Output details to CLI) | `-d` (and optional `-u`) |
| **7** | **Launch GUI** | None |

#### CLI Examples

1.  **Run Top Readers analysis:**
    ```bash
    python main.py -f data/issuu_sample.json -t 4
    ```
2.  **Run Views by Country for a specific document:**
    ```bash
    python main.py -f data/issuu_sample.json -t 2a -d 99d86016149c4f45b7f21223e74c8b6d
    ```

-----

### 2\. Graphical User Interface (GUI)

The GUI provides a visual interface for all tasks, rendering histograms and the Also Likes graph using Matplotlib.

#### Launching the GUI (Task 7)

```bash
python main.py -f data/issuu_sample.json -t 7
```

#### GUI Controls

  * **Inputs:** Enter **Document UUID** and **Visitor UUID** at the top.
  * **Left Panel:** Displays text output for analytical tasks (e.g., Top Readers, Also Likes list).
  * **Right Panel:** Displays graphical output (Histograms, Network Graph).

-----

## 🛠️ Project Structure

| File | Description | Key Features |
| :--- | :--- | :--- |
| `main.py` | **CLI Driver.** Uses `argparse` to handle command-line inputs and executes the specified task. | Contains logic for printing results in a readable CLI format. |
| `dataloader.py` | **Data Access Layer.** Handles file I/O. | Uses a **generator function** (`yield`) for memory-efficient, line-by-line reading of large JSON files. |
| `analysis.py` | **Core Business Logic.** Contains all analytics functions. | Implements logic for geo-analysis, browser parsing, reader time aggregation, and the **parametrised "Also Likes"** recommendation system (Task 5c). Uses `networkx` for graph generation (Task 6). |
| `gui.py` | **User Interface.** Builds the Tkinter application. | Integrates all analysis functions and embeds Matplotlib visualizations (histograms, graph) into the window. |
| `continents.py` | **Configuration.** | Contains the country-to-continent mapping dictionary. |
| `data/issuu_sample.json` | **Input Data.** | The required data file (not provided in this repository, must be added by the user). |

-----

## Key Design Features

  * **Scalability (Functional Programming):** The `dataloader.py` uses **Python generators** to process the data stream line-by-line, preventing memory-based issues when dealing with large datasets (millions of lines).
  * **Flexibility (Higher-Order Functions):** The core recommendation function, `also_likes_documents` (Task 5c), accepts a **sorting function** as a parameter. This allows the ranking criteria (e.g., shared readers, weighted by document length, etc.) to be changed easily without altering the main logic.
  * **Graph Analysis (NetworkX):** The "Also Likes" relationship (Task 6) is modeled using the `networkx` library, which is then visualized in the GUI, providing a powerful structure for link analysis.
