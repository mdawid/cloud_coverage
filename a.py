from bs4 import BeautifulSoup
from datetime import datetime
import re
import requests

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
}

page = requests.get("https://www.meteoblue.com/pl/pogoda/outdoorsports/seeing/podlesie_polska_3088637", headers=headers)
content = page.content

# read the HTML file
#with open('a.html', 'r', encoding='ISO-8859-2') as file:
#    content = file.read()

# parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# define the list to hold all the data
data = []

# initialize date to None
date_str = None

# find all 'table' elements
table = soup.find('table')
tbody = table.find('tbody')

# find all 'tr' elements with class="hour-row" in the table, these are the rows containing the hourly data
hour_rows = tbody.find_all('tr', attrs={'data-hour': True})

for hour_row in hour_rows:
    # read date row
    if date_str is None:
        prev_tr = hour_row
        for _ in range(5):
            prev_tr = prev_tr.find_previous_sibling()
            if prev_tr:
                new_day = prev_tr.find('td', {'class' : 'new-day'})
                if new_day is not None:
                    date_str = re.search(r'\d{4}-\d{2}-\d{2}', new_day.text).group()
                    break
            else:
                break
    
    # get all the 'td' elements in the row
    tds = hour_row.find_all('td')
    
    # check if all necessary 'td' elements are present
    if len(tds) >= 4:
        # get the hour from the first 'td' element
        hour = tds[0].text.strip()

        # get the low, mid, high cloud coverage from the next three 'td' elements
        low_cloud_coverage = tds[1].text.strip()
        mid_cloud_coverage = tds[2].text.strip()
        high_cloud_coverage = tds[3].text.strip()
    
    # add the date, hour, and cloud coverages to the data list
    date = datetime.strptime(date_str, '%Y-%m-%d').replace(hour=int(hour))

    data.append([date, low_cloud_coverage, mid_cloud_coverage, high_cloud_coverage])

    if hour == "23":
        date_str = None

# Print the table with tab-separated values
for row in data:
    print('\t'.join(str(value) for value in row))

# write the DataFrame to a CSV file
#df.to_csv('cloud_coverage.csv', index=False)
