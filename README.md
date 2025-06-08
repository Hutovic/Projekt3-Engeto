#Elections Scraper – Poslanecká sněmovna ČR 2017

Tento projekt je součástí třetího závěrečného zadání v rámci kurzu Engeto Online Python Akademie. Slouží ke scrapování volebních výsledků pro jednotlivé obce z webu https://www.volby.cz a exportu výsledků do `.csv` souboru.

##Obsah výstupního souboru `.csv`

Každý řádek ve výstupním souboru obsahuje informace o konkrétní obci:
1. Kód obce
2. Název obce
3. Počet voličů v seznamu
4. Počet vydaných obálek
5. Počet platných hlasů
6. Počet hlasů pro každou kandidující stranu (každá strana má vlastní sloupec)

---

##Požadavky

- Python 3.8+
- Internetové připojení

---

##Instalace závislostí

Nejprve doporučuji vytvořit si virtuální prostředí (není povinné, ale doporučeno):

```bash
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows
```

Nainstalujte potřebné knihovny pomocí `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

##Spuštění programu

Program se spouští pomocí dvou argumentů:

```bash
python main.py <URL> <název_výstupního_souboru.csv>
```

Např.:

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledky_benesov.csv"
```

---

##Ošetření vstupu

Pokud není zadán správný počet argumentů nebo není URL platná, program vypíše chybovou hlášku a ukončí se:

```
Použití: python main.py <URL> <výstupní_soubor.csv>
Ujisti se, že první argument je správná URL začínající na 'https://www.volby.cz/pls/ps2017nss/ps32'
```

---

##Ukázka výstupu

Spuštění příkazu:

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledky.csv"
```

Výstup:

```text
Nájdených obcí: 139
Prvý odkaz: https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=530760&xvyber=2101
Teplýšovice spracovaná
Bílkovice spracovaná
...
```

Ukázka dat ve výstupním souboru `.csv`:

| kód obce | obec       | voliči | obálky | platné hlasy | Občanská demokratická strana | ... |
|----------|------------|--------|--------|----------------|-------------------------------|-----|
| 530760   | Teplýšovice    | 383  | 289   | 288           | 22                          | ... |
| 530743   | Čechtice   | 170   | 121    | 118            | 7                            | ... |

---

##Autor

Tomáš Hutňan 
`tomas.hutnan@internationalsos.com`  
Červen 2025
