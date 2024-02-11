import requests
from bs4 import BeautifulSoup
import csv

url = 'https://upcfoodsearch.com/food-ingredients/'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main div with class "panel list-group lg-root well"
    main_div = soup.find('div', class_='panel list-group lg-root well')

    # Find all divs with id from A to Z
    alphabetic_divs = main_div.find_all('div', id=lambda x: x and x.isalpha())

    # Create a CSV file and write the header
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Name', 'Link', 'Source(s) Derived From', 'Natural or Artificial?'])

        # Iterate through each alphabetic div
        for alphabetic_div in alphabetic_divs:
            # Find all anchor tags within the div
            anchor_tags = alphabetic_div.find_all('a')

            # Iterate through each anchor tag
            for anchor_tag in anchor_tags:
                name = anchor_tag.text.strip()
                link = anchor_tag['href']

                # Send a GET request to the link
                link_response = requests.get(link)

                # Check if the request to the link was successful
                if link_response.status_code == 200:
                    # Parse the linked page using BeautifulSoup
                    link_soup = BeautifulSoup(link_response.content, 'html.parser')

                    # Find the div with class "table-responsive"
                    table_div = link_soup.find('div', class_='table-responsive')

                    # Find the table with class "table table-striped"
                    data_table = table_div.find('table', class_='table table-striped')

                    # Find the rows in the table
                    rows = data_table.find_all('tr')

                    # Initialize variables to store data
                    source_from = ''
                    natural_or_artificial = ''

                    # Iterate through each row in the table
                    for row in rows:
                        h3_tag = row.find('h3')

                        if h3_tag:
                            header_text = h3_tag.text.strip()

                            # Check for specific headers and extract data
                            if header_text == 'Source(s) Derived From':
                                source_from = row.find_all('td')[1].text.strip()
                            elif header_text == 'Natural or Artificial?':
                                natural_or_artificial = row.find_all('td')[1].text.strip()

                    # Write data to CSV
                    csv_writer.writerow([name, link, source_from, natural_or_artificial])
                    print(f'Data for {name}:')
                    print(f' - Link: {link}')
                    print(f' - Source(s) Derived From: {source_from}')
                    print(f' - Natural or Artificial?: {natural_or_artificial}')
                    print('-' * 30)

                else:
                    print(f'Failed to retrieve data from {link}. Status code:', link_response.status_code)

    print('All data scraped and saved to output.csv')
else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)