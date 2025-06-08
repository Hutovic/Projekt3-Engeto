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

# ===== Validácia argumentov =====
if len(sys.argv) != 3:
    print("Chyba: Musíte zadať 2 argumenty – URL a názov CSV súboru.")
    print("Použitie: python main.py \"URL\" \"vystup.csv\"")
    sys.exit(1)

url = sys.argv[1]
output_file = sys.argv[2]

# Kontrola, že URL vyzerá ako výber obcí (musí obsahovať 'ps32')
if "ps32" not in url:
    print("Chyba: Zadaná URL neodkazuje na stránku so zoznamom obcí (ps32).")
    sys.exit(1)

# Získanie HTML stránky
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# Nájde odkazy na všetky obce z viacerých tabuliek
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

# ===== Získanie zoznamu strán =====
def extract_parties(soup):
    parties = {}
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        for row in rows:
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

# Zistíme názvy strán z prvej obce
first_obec_html = requests.get(obec_links[0])
first_obec_html.encoding = 'utf-8'
first_soup = BeautifulSoup(first_obec_html.text, 'html.parser')
first_parties = extract_parties(first_soup)
party_names = list(first_parties.keys())

# ===== Zápis do CSV =====
with open(output_file, mode='w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    header = ['kód obce', 'obec', 'voliči', 'obálky', 'platné hlasy'] + party_names
    writer.writerow(header)

    for link in obec_links:
        try:
            res = requests.get(link)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')

            # Získanie kódu obce z URL
            code = parse_qs(urlparse(link).query).get('xobec', [''])[0]

            # Získanie názvu obce
            h3_tags = soup.find_all('h3')
            location = ''
            for tag in h3_tags:
                if "Obec:" in tag.text:
                    location = tag.text.replace('Obec:', '').strip()
                    break

            registered = soup.find('td', {'headers': 'sa2'}).text.replace('\xa0', '').strip()
            envelopes = soup.find('td', {'headers': 'sa5'}).text.replace('\xa0', '').strip()
            valid = soup.find('td', {'headers': 'sa6'}).text.replace('\xa0', '').strip()

            # Hlasy pre strany
            parties = extract_parties(soup)
            votes = [parties.get(name, '0') for name in party_names]

            writer.writerow([code, location, registered, envelopes, valid] + votes)
            print(f"{location} spracovaná")

        except Exception as e:
            print(f"Chyba v {link}: {e}")
