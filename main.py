
"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Tomáš Hutňan
email: tomas.hutnan@internationalsos.com
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, parse_qs

def validate_arguments():
    if len(sys.argv) != 3:
        print("Chyba: Musíte zadať 2 argumenty – URL a názov CSV súboru.")
        print("Použitie: python main.py \"URL\" \"vystup.csv\"")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    if "ps32" not in url:
        print("Chyba: Zadaná URL neodkazuje na stránku so zoznamom obcí (ps32).")
        sys.exit(1)

    return url, output_file

def get_obec_links(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table', {'class': 'table'})
    if not tables:
        print("Chyba: Na stránke nebola nájdená žiadna tabuľka s obcami.")
        sys.exit(1)

    links = []
    for table in tables:
        links += table.find_all('a')

    base_url = "https://www.volby.cz/pls/ps2017nss/"
    obec_links = list(set(base_url + link['href'] for link in links))

    if not obec_links:
        print("Chyba: Na stránke neboli nájdené žiadne odkazy na obce.")
        sys.exit(1)

    print(f"Nájdených obcí: {len(obec_links)}")
    print(f"Prvý odkaz: {obec_links[0]}")

    return obec_links

def extract_parties(soup):
    parties = {}
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) >= 3:
                try:
                    name = cols[1].text.strip()
                    votes = cols[2].text.strip().replace("\xa0", "")
                    if name and not name.isdigit() and name not in parties:
                        parties[name] = votes
                except:
                    continue
    return parties

def extract_municipality_data(link, party_names):
    try:
        res = requests.get(link)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        code = parse_qs(urlparse(link).query).get('xobec', [''])[0]

        location = ''
        for tag in soup.find_all('h3'):
            if "Obec:" in tag.text:
                location = tag.text.replace('Obec:', '').strip()
                break

        registered = soup.find('td', {'headers': 'sa2'}).text.replace('\xa0', '').strip()
        envelopes = soup.find('td', {'headers': 'sa5'}).text.replace('\xa0', '').strip()
        valid = soup.find('td', {'headers': 'sa6'}).text.replace('\xa0', '').strip()

        parties = extract_parties(soup)
        votes = [parties.get(name, '0') for name in party_names]

        print(f"{location} spracovaná")
        return [code, location, registered, envelopes, valid] + votes

    except Exception as e:
        print(f"Chyba v {link}: {e}")
        return None

def main():
    url, output_file = validate_arguments()
    obec_links = get_obec_links(url)

    first_obec_html = requests.get(obec_links[0])
    first_obec_html.encoding = 'utf-8'
    first_soup = BeautifulSoup(first_obec_html.text, 'html.parser')
    party_names = list(extract_parties(first_soup).keys())

    with open(output_file, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        header = ['kód obce', 'obec', 'voliči', 'obálky', 'platné hlasy'] + party_names
        writer.writerow(header)

        for link in obec_links:
            row = extract_municipality_data(link, party_names)
            if row:
                writer.writerow(row)

if __name__ == "__main__":
    main()
