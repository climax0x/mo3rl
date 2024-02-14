from duckduckgo_search import DDGS
from urllib.parse import urlparse
import math
import time

def extract_domain(href):
    parsed_url = urlparse(href)
    domain = parsed_url.netloc.split(':')[0]  # Extract domain name from parsed URL
    if domain.startswith("www."):  # Check if the domain starts with "www."
        domain = domain[4:]  # Remove "www." prefix
    return domain

if __name__ == "__main__":
    try:
        query = input("Enter search query: ")
        retry_attempts = 3  # Number of retry attempts
        current_attempt = 1
        
        while current_attempt <= retry_attempts:
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(query, max_results=1000)]  # Set max_results to a large number
                num_results = len(results)
                num_pages = math.ceil(num_results / 10)  # Assuming 10 results per page
                
                if results:
                    print(f"Total number of search results: {num_results}")
                    print(f"Estimated number of pages in results: {num_pages}")
                    print("\nSearch Results:")
                    unique_domains = set()
                    for result in results:
                        domain = extract_domain(result['href'])
                        unique_domains.add(domain)
                    print("\nUnique Domains:")
                    for domain in unique_domains:
                        print(domain)
                    break
                else:
                    print("No search results found.")
                    
            if current_attempt < retry_attempts:
                print(f"Retry attempt {current_attempt} in 1 minute...")
                time.sleep(60)  # Sleep for 1 minute before retrying
                current_attempt += 1
            else:
                print("Exceeded maximum retry attempts. Exiting...")
                break
                
    except Exception as e:
        print(f"An error occurred: {e}")
