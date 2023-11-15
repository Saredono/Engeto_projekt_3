"""
python_projekt3.py: třetí projekt do Engeto Online Python Akademie
author: Tomáš Golasowski
email: golasowski.tomas@gmail.com
discord: Tomáš G.
"""



import sys
import csv
import requests
from bs4 import BeautifulSoup

# zkontroluje počet zadaných argumentů
def check_num_of_args():
    if len(sys.argv) != 3:
        print('Wrong input, use this order: script.py <town_link> <output_file.csv>')
        sys.exit()

# zkontroluje zadané url
def check_town_link(link):
    print('Checking the provided town link...')
    try:
        district_url = []
        html = get_soup('https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ')
        for i in range(15):
            district_url_soup = html.find_all('td', headers=f't{i}sa3')
            for dis in district_url_soup:
                dis = dis.a['href']
                district_url.append(f'https://www.volby.cz/pls/ps2017nss/{dis}')

        if link not in district_url:
            print(f'Wrong town link')
            print(f'Choose from here: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ')
            quit()
        else:
            print('Provided town link is valid.')

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the district URLs: {e}")
        quit()
    
    

# získá soup z URL
def get_soup(url):
    print(f' data from {url}')
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


# získá data z URL
def get_data_from_link(link):
    print('Extracting data from the town link...')
    data = []
    soup = get_soup(link)
    for row in soup.find_all('tr')[2:]:  # vyhne se iteraci nadpisů v tabulce ( první 2 řady)
        cells = row.find_all('td')
        if len(cells) > 1:  
            location_code = cells[0].text
            location = cells[1].text.strip()
            # zkontroluje existenci a tagu, než začne přistupovat  k href tagu
            a_tag = cells[0].find('a')
            if a_tag and 'href' in a_tag.attrs:
                location_url_suffix = a_tag['href']
                location_url = f'https://volby.cz/pls/ps2017nss/{location_url_suffix}'
                location_soup = get_soup(location_url)
            
        
                registered_voters = location_soup.find('td', headers='sa2').text.replace('\xa0', ' ')
                envelopes = location_soup.find('td', headers='sa3').text.replace('\xa0', ' ')
                valid_votes = location_soup.find('td', headers='sa6').text.replace('\xa0', ' ')
            
                votes = []
                for vote_header in ['t1sb3', 't2sb3']:
                    vote_cells = location_soup.find_all('td', headers=vote_header)
                    for vote_cell in vote_cells:
                        vote = vote_cell.text.replace('\xa0', ' ')
                        if vote != '-':
                            votes.append(vote)
            else:
                continue  # přeskočí data, kde není odkaz ( prázdné buňky, nadpisy atd.)

            row_data = [location_code, location, registered_voters, envelopes, valid_votes] + votes
            data.append(row_data)
    print('Data extraction complete.')
    return data

# vypíše data do csv
def write_to_csv(filename, header, data):
    print(f'Writing data to {filename}...')
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        for row in data:
            csvwriter.writerow(row)
    print(f'Data successfully written to {filename}.')

# main funkce
def main(link, filename):
    check_town_link(link)
   
    
    first_link = get_soup(link).find('td', 'cislo').a['href']
    first_link_url = f'https://volby.cz/pls/ps2017nss/{first_link}'
    parties = [party.text for party in get_soup(first_link_url).find_all('td', 'overflow_name')]
    
    header = ['Code', 'Location', 'Registered Voters', 'Envelopes', 'Valid Votes'] + parties
    data = get_data_from_link(link)
    
    write_to_csv(filename, header, data)
    
#zkontroluje argumenty před spuštěním funkce
check_num_of_args()

if __name__ == '__main__':
    print('Starting the script...')
    link = sys.argv[1]
    filename = sys.argv[2]
    main(link, filename)
    print('Script finished.')
