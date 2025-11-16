from dataloader import load_data
from analysis import views_by_country, views_by_continent, show_histogram, top_readers

file_path = "./data/issuu_sample.json"
doc_id = input("Enter document UUID: ")

# Country histogram
country_result = views_by_country(doc_id, file_path)
print("\nCountry views:", country_result)
show_histogram(country_result, "Views by Country")

# Continent histogram
continent_result = views_by_continent(doc_id, file_path)
print("\nContinent views:", continent_result)
show_histogram(continent_result, "Views by Continent")

# Top 10 readers
top10 = top_readers(file_path)
print("\nTop 10 Readers (visitor_uuid, total_time):")
for user, time in top10:
    print(user, " → ", time, "seconds")