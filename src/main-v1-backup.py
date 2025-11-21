from dataloader import load_data
from analysis import views_by_country, views_by_continent, show_histogram, top_readers, views_by_browser_full, views_by_browser_main

file_path = "../data/issuu_sample.json"
doc_id = input("Enter document UUID: ")

# Country histogram
country_result = views_by_country(doc_id, file_path)
print("\nCountry views:", country_result)
show_histogram(country_result, "Views by Country")

# Continent histogram
continent_result = views_by_continent(doc_id, file_path)
print("\nContinent views:", continent_result)
show_histogram(continent_result, "Views by Continent")

# --------------------------------------------------------

# Browser histogram (Full User Agent) - Task 3a
browser_full_result = views_by_browser_full(file_path)
print("\nViews by Full Browser User Agent (Top 10):", dict(sorted(browser_full_result.items(), key=lambda item: item[1], reverse=True)[:10]))
show_histogram(dict(sorted(browser_full_result.items(), key=lambda item: item[1], reverse=True)[:10]), "Views by Full Browser User Agent (Top 10)")

# Browser histogram (Main Browser Name) - Task 3b
browser_main_result = views_by_browser_main(file_path)
print("\nViews by Main Browser Name:", browser_main_result)
show_histogram(browser_main_result, "Views by Main Browser Name")

# --------------------------------------------------------

# Top 10 readers
top10 = top_readers(file_path)
print("\nTop 10 Readers (visitor_uuid, total_time):")
for user, time in top10:
    print(user, " → ", time, "seconds")