from dataloader import load_data
import re



def views_by_browser_full(file_path):
    browser_counter = {}
    for record in load_data(file_path):
        user_agent = record.get("visitor_useragent")
        if user_agent:
            browser_counter[user_agent] = browser_counter.get(user_agent, 0) + 1
    return browser_counter

def extract_main_browser(user_agent):
    if not user_agent:
        return "Unknown"

    browsers = ["Firefox", "Chrome", "Safari", "Opera", "Edge", "IE", "Mozilla"]

    for browser in browsers:
        match = re.search(fr'{re.escape(browser)}[/ ]\d+', user_agent, re.IGNORECASE)
        if match:
            return browser
        
    return "Other"

def views_by_browser_main(file_path):
    browser_counter = {}
    
    full_agents_counts = views_by_browser_full(file_path)

    for user_agent, count in full_agents_counts.items():
        main_browser = extract_main_browser(user_agent)
        browser_counter[main_browser] = browser_counter.get(main_browser, 0) + count
        
    return browser_counter

