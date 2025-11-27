from dataloader import load_data
import re
from collections import Counter

# INTERNAL HELPERS

def _count_all_full_agents(file_path):
    # Counts all unique full user agents from the dataset.
    browser_counter = Counter()
    for record in load_data(file_path):
        user_agent = record.get("visitor_useragent")
        if user_agent:
            browser_counter[user_agent] += 1
    return browser_counter

def _describe_user_agent(user_agent):
    # Creates a concise, readable description for a legend/mapping.
    if not user_agent:
        return "Unknown Agent"

    main_browsers = ["Firefox", "Chrome", "Safari", "Opera", "Edge", "IE", "Mozilla", "Trident"]
    browser_part = "Unknown"
    version_part = ""
    
    for browser in main_browsers:
        match = re.search(fr'({re.escape(browser)})[/ ](\d+\.\d+)', user_agent, re.IGNORECASE)
        if match:
            browser_part = match.group(1)
            version_part = match.group(2)
            break
            
    match_os = re.search(r'\((.*?)\)', user_agent)
    os_part = ""
    if match_os:
        os_info = match_os.group(1).split(';')[0].strip().replace('_', ' ')
        os_part = f" on {os_info}"

    return f"{browser_part} {version_part}{os_part}" if version_part else f"{browser_part}{os_part}"

# -------------------------------------------------------------------------
# Task `3a`: Views by browser full
# -------------------------------------------------------------------------

def views_by_browser_full(file_path):
    return dict(_count_all_full_agents(file_path))

# -------------------------------------------------------------------------
# Task `3a_part` Plot-Friendly: Top N + Tags/Legend (The New 3a_part) ---
# -------------------------------------------------------------------------

def views_by_browser_full_plot_friendly(file_path, top_n=10):
    #
    #Returns the Top N most frequent specific user agents using short tags 
    #for clean plotting, with a separate dictionary for the legend.
    
    #Returns: (tagged_counts_dict, tag_mapping_dict)
    full_agent_counts = _count_all_full_agents(file_path)
    top_agents = full_agent_counts.most_common(top_n)
    
    tagged_counts = {}
    tag_mapping = {}
    tag_index = 1
    
    for full_agent, count in top_agents:
        tag = f"A{tag_index:02d}"
        description = _describe_user_agent(full_agent)
        
        tagged_counts[tag] = count
        tag_mapping[tag] = description
        
        tag_index += 1

    top_n_views_sum = sum(tagged_counts.values())
    total_views = sum(full_agent_counts.values())
    other_views = total_views - top_n_views_sum

    if other_views > 0:
        tagged_counts["OTHER"] = other_views
        tag_mapping["OTHER"] = "All other low-volume user agents"
        
    return tagged_counts, tag_mapping


# -------------------------------------------------------------------------
# Task 3b: Views by Main Browser Name
# -------------------------------------------------------------------------

def extract_main_browser(user_agent):
    if not user_agent:
        return "Unknown"

    browsers = ["Firefox", "Chrome", "Safari", "Opera", "Edge", "IE", "Mozilla"]

    for browser in browsers:
        # Searches for 'BrowserName/' or 'BrowserName ' followed by a digit (version)
        if re.search(fr'{re.escape(browser)}[/ ]\d+', user_agent, re.IGNORECASE):
            return browser
        
    return "Other"

def views_by_browser_main(file_path):
    full_agents_counts = _count_all_full_agents(file_path)

    browser_counter = Counter()
    for user_agent, count in full_agents_counts.items():
        main_browser = extract_main_browser(user_agent)
        browser_counter[main_browser] += count
        
    return dict(browser_counter)
