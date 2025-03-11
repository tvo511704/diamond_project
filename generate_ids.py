from selenium import webdriver
from bs4 import BeautifulSoup
import itertools
import time

# Output files
output_file_1 = 'diamond_ids.txt'  # Real-time output of diamond IDs
output_file_2 = 'summary.txt'  # Real-time summary information

# Function to scrape a single page
def scrape_page(clarity, color, cut, page_number, driver, output_summary):
    base_url = (f'https://www.bluenile.com/diamond-search?resultsView=List&page={page_number}'
                f'&CaratFrom=0.3&Color={color}&Clarity={clarity}&Cut={cut}'
                f'&FluorescenceToggle=yes&PolishToggle=yes&SymmetryToggle=yes&CertificateToggle=yes')
    try:
        driver.get(base_url)
        time.sleep(3)  # Allow time for the page to load
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Extract Diamond IDs
        results = soup.find_all('a', href=True)
        diamond_ids = [
            result['href'].split('/diamond-details/')[-1].split('?')[0]
            for result in results if '/diamond-details/' in result['href']
        ]

        # Write real-time summary to Output 2
        with open(output_summary, 'a') as summary_file:
            summary_file.write(f"Page {page_number}, {len(diamond_ids)} IDs, Clarity={clarity}, Color={color}, Cut={cut}\n")

        # Real-time log to terminal
        print(f"Page {page_number} - Found {len(diamond_ids)} IDs for Clarity={clarity}, Color={color}, Cut={cut}")
        return diamond_ids
    except Exception as e:
        print(f"Error scraping page {page_number} for Clarity={clarity}, Color={color}, Cut={cut}: {e}")
        return []

# Main script
clarity_values = ['SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF', 'FL']
color_values = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
cut_values = ['AstorIdeal', 'Ideal', 'Very+Good', 'Good']

combinations = itertools.product(clarity_values, color_values, cut_values)
unique_ids = set()  # Use a set to store unique diamond IDs

driver = webdriver.Chrome()

# Clear output files before running
open(output_file_1, 'w').close()
open(output_file_2, 'w').close()

try:
    for clarity, color, cut in combinations:
        page_number = 1
        while True:
            diamond_ids = scrape_page(clarity, color, cut, page_number, driver, output_file_2)
            
            if not diamond_ids:  # Stop if no IDs are found on the page
                break
            
            # Real-time write to Output 1
            with open(output_file_1, 'a') as f:
                for diamond_id in diamond_ids:
                    f.write(diamond_id + '\n')

            unique_ids.update(diamond_ids)  # Add to the set
            page_number += 1
finally:
    driver.quit()

# Final logs
print(f"Expected unique diamond IDs: 93,955")
print(f"Actual unique diamond IDs: {len(unique_ids)}")
print(f"Diamond IDs successfully exported to {output_file_1}")
print(f"Summary information successfully exported to {output_file_2}")
