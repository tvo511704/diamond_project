import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

# Define a function to extract diamond details
def extract_diamond_details(diamond_id):
    url = f"https://www.bluenile.com/diamond-details/{diamond_id}"
    
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        response.raise_for_status()
    except requests.exceptions.TooManyRedirects:
        print(f"Too many redirects for Diamond ID {diamond_id}.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for Diamond ID {diamond_id}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract details with improved HTML structure parsing
    try:
        # Check for each element, ensuring it exists before accessing its .text
        product_name = soup.find('h1', attrs={"data-qa": "title-itemPage"})
        if product_name:
            product_name = product_name.text.strip()
        else:
            product_name = "N/A"

        price = soup.find('div', class_='price--GUo2yxzV2va4P7Bqe00G')
        if price:
            price = price.text.strip()
        else:
            price = "N/A"

        color = soup.find('div', {'data-qa': lambda x: x and x.startswith('Color-')})
        if color:
            color = color.text.strip()
        else:
            color = "N/A"

        cut = soup.find('div', {'data-qa': lambda x: x and x.startswith('Cut-')})
        if cut:
            cut = cut.text.strip()
        else:
            cut = "N/A"

        clarity = soup.find('div', {'data-qa': lambda x: x and x.startswith('Clarity-')})
        if clarity:
            clarity = clarity.text.strip()
        else:
            clarity = "N/A"

        polish = soup.find('div', {'data-qa': lambda x: x and x.startswith('polish-')})
        if polish:
            polish = polish.text.strip()
        else:
            polish = "N/A"

        symmetry = soup.find('div', {'data-qa': lambda x: x and x.startswith('symmetry-')})
        if symmetry:
            symmetry = symmetry.text.strip()
        else:
            symmetry = "N/A"

        shape = soup.find('div', {'dataqa': lambda x: x and x.startswith('Shape-')})
        if shape:
            shape = shape.text.strip()
        else:
            shape = "N/A"

        carat_weight = soup.find(text="Carat Weight")
        if carat_weight:
            carat_weight = carat_weight.find_next().text.strip()
        else:
            carat_weight = "N/A"

        fluorescence = soup.find(text="Fluorescence")
        if fluorescence:
            fluorescence = fluorescence.find_next().text.strip()
        else:
            fluorescence = "N/A"

    except AttributeError as e:
        print(f"Failed to parse details for Diamond ID {diamond_id}: {e}")
        return None

    return {
        "Diamond ID": diamond_id,
        "Product Name": product_name,
        "Price": price,
        "Shape": shape,
        "Color": color,
        "Cut": cut,
        "Clarity": clarity,
        "Polish": polish,
        "Symmetry": symmetry,
        "Carat Weight": carat_weight,
        "Fluorescence": fluorescence,
    }

# Function to process a text file with diamond IDs
def process_txt(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        with open(file_path, 'r') as file:
            diamond_ids = file.read().splitlines()  # Read diamond IDs from each line
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    # Prepare output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"diamond_detail_{timestamp}.csv"
    try:
        pd.DataFrame(columns=[
            "Diamond ID", "Product Name", "Price", "Shape", "Color", "Cut", "Clarity", "Polish", "Symmetry", "Carat Weight", "Fluorescence"
        ]).to_csv(output_file, index=False)
        print(f"Initialized output file: {output_file}")
    except Exception as e:
        print(f"Failed to initialize output file: {e}")
        return

    results = []
    for i, diamond_id in enumerate(diamond_ids, start=1):
        print(f"Processing Diamond ID: {diamond_id}")
        details = extract_diamond_details(diamond_id)
        if details:
            results.append(details)

        # Save batch every 1000 records
        if i % 1000 == 0 or i == len(diamond_ids):
            try:
                pd.DataFrame(results).to_csv(output_file, mode='a', header=False, index=False)
                print(f"Saved {len(results)} records to {output_file}")
                results = []  # Clear the batch
            except Exception as e:
                print(f"Failed to save batch to CSV: {e}")

# Example usage
if __name__ == "__main__":
    file_path = "diamond_ids.txt"
    process_txt(file_path)
