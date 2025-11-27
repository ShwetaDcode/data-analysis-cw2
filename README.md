## Document Tracker Analytics

This repository contains the source code for a data-intensive Python application designed to analyze document tracking data, such as that from the **issuu.com** platform. The application includes both a Command-Line Interface (CLI) for batch processing and a Graphical User Interface (GUI) for interactive visualization.

---

## Getting Started

### Prerequisites

- **Python 3.x**
- **Required Python Libraries:**
  - `networkx`
  - `matplotlib`
  - `tkinter` (usually bundled with Python)

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

---

## Usage

The application can be executed in two modes: **Command-Line (CLI)** or **Graphical User Interface (GUI)**.

### 1\. Command-Line Interface (CLI)

Use `main.py` to run specific analysis tasks, which is ideal for scripting and testing.

#### Syntax

```bash
python main.py -f <file_name> -t <task_id> [-d <doc_uuid>] [-u <user_uuid>]
```

| Argument          | Description                                       | Required | Example                  |
| :---------------- | :------------------------------------------------ | :------- | :----------------------- |
| `-f, --file_name` | Path to the JSON input file.                      | **Yes**  | `data/issuu_sample.json` |
| `-t, --task_id`   | The analysis task to execute.                     | **Yes**  | `2a`, `3b`, `5d`, `7`    |
| `-d, --doc_uuid`  | Document UUID (required for Tasks 2a, 2b, 5d, 6). | No       | `1a2b3c4d5e6f`           |
| `-u, --user_uuid` | Visitor UUID (optional for Tasks 5d, 6).          | No       | `9x8y7z6w`               |

#### Available Task IDs (`-t`)

| Task ID | Description                                         | Required Arguments       |
| :------ | :-------------------------------------------------- | :----------------------- |
| **2a**  | Views by Country                                    | `-d`                     |
| **2b**  | Views by Continent                                  | `-d`                     |
| **3a**  | Views by Full Browser User Agent                    | None                     |
| **3b**  | Views by Main Browser Name                          | None                     |
| **4**   | Top 10 Readers (by total read time)                 | None                     |
| **5d**  | Also Likes (Top 10 Documents by Shared Readers)     | `-d` (and optional `-u`) |
| **6**   | Also Likes Graph Generation (Output details to CLI) | `-d` (and optional `-u`) |
| **7**   | **Launch GUI**                                      | None                     |

#### CLI Examples

**TASK 2A – Views by country**
python cw2.py -d 140219141540-c900b41f845c67cc08b58911155c681c -t 2a -f ./data/issuu_sample.json

**TASK 2B – Views by continent**
python cw2.py -d 140219141540-c900b41f845c67cc08b58911155c681c -t 2b -f ./data/issuu_sample.json

**TASK 3A – Views by full browser**
python cw2.py -t 3a -f data/issuu_sample.json

**TASK 3B – Views by main browser**
python cw2.py -t 3b -f data/issuu_sample.json

**TASK 4 – Top readers**
python cw2.py -t 4 -f ./data/issuu_sample.json

**TASK 5D – Also likes**
python cw2.py -u 88c39a2a81272740 -d 140219141540-c900b41f845c67cc08b58911155c681c -t 5d -f ./data/issuu_sample.json

**TASK 7 – Launch GUI**
python cw2.py -t 7 -f ./data/issuu_sample.json

#### GUI Controls

- **Inputs:** Enter **Document UUID** and **Visitor UUID** at the top.
- **Left Panel:** Displays text output for analytical tasks (e.g., Top Readers, Also Likes list).
- **Right Panel:** Displays graphical output (Histograms, Network Graph).

exe controls cw2.exe
.\cw2.exe -t 7 -f data/issuu_sample.json
