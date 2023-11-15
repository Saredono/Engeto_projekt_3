**Engeto_projekt_3**

Tento projekt slouží k extrahování dat jednotlivých volebních okresů z parlamentních voleb v roce 2017.

Knihovny, které je nutné mít nainstalované pro správné spuštění skriptu jsou uvedeny v souboru requirements.txt. Pro instalaci doporučuji použít  virtuální prostředí, kde se všechny knihovny nainstalují pomocí: $ pip3 install -r requirements.txt

**Spuštění projektu**

Spuštění programu scraper.py v příkazovém řádku požaduje dva povinné argumenty – odkaz na stránku okresu, který chceme extrahovat a výstupní CSV soubor.

Př. použití: python scraper.py [odkaz územního celku] [výsledný soubor]. Data z uvedeného odkazu se stáhnou a uloží do souboru CSV. Odkaz je nutné zadávat v plné délce, tedy https://www.volby.cz/... a CSV soubor je možné pojmenovat libovolně.

**Ukázka**

Výsledky hlasování pro okres Sokolov:

Program spustím přes tyto argumenty: 

python scraper.py  "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4103" Sokolov.csv
