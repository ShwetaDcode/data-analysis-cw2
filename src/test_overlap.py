from dataloader import load_data

file = "data/issuu_sample.json"

user_docs = {}

# build mapping: user -> set of documents read
for rec in load_data(file):
    u = rec.get("visitor_uuid")
    d = rec.get("subject_doc_id")
    event = rec.get("event_type")

    if event in {"read", "pageread", "pagereadtime"}:
        if u and d:
            user_docs.setdefault(u, set()).add(d)

# Check overlaps
overlap_count = 0
for u, docs in user_docs.items():
    if len(docs) > 1:
        print("User", u, "read multiple docs:", docs)
        overlap_count += 1

print("\nTotal users with multiple document reads:", overlap_count)
