from dataloader import load_data
from collections import Counter

file = "./data/issuu_sample.json"

def top_documents(file_path, limit=10):
    counter = Counter()

    for rec in load_data(file_path):
        if rec.get("event_type") in ("read", "pagereadtime"):
            doc = rec.get("subject_doc_id")
            counter[doc] += 1

    return counter.most_common(limit)


if __name__ == "__main__":
    print("\nTop documents by number of readers:\n")
    for doc, count in top_documents(file, 10):
        print(doc, "=>", count, "reads")
