# Diaken Diensbeurte

Hierdie program skep diaken diensbeurte in 'n totaal lukrake en regverdige manier.

Die inset is 'n lys diakens (`./diakens.txt`) en die uitset is 'n paar PDF en CSV lêers (`./data/x.pdf` en `./data/x.csv`).

## Stel omgewing op
Hardloop die volgende instruksies:

Linux / macOS
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows:
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Hoe om te gebruik?
Doen gewoon `python main.py`. Dit sal diaken diensbeurte vir die volgende 4 maande uitwerk.

Daar is opsies beskikbaar wat u sal toelaat om die hoeveelheid maande en indelingstrategie te verander. Vir meer inligting sien `python main.py --help`.

'n Opsomming van die opsies:
- -m, --maande: Hoeveelheid maande om die diensbeurte uit te werk.
    - Verstekwaarde is 4.
- -hm, --huidige-maand: Begin met die huidige maand in plaas van die volgende maand.
- -s, --strategie: Strategie vir indeling.
    - 1: Lukraak.
    - 2: Gebruik huidige volgorde.

## Hoe werk die indeling?
Die hele diakenlys word geshuffel (volgens die [Fisher-Yates algoritme](https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle)), daarna word die name sekwensieel in groepe van 4 per Sondag ingedeel. Elke Sondag se 4 name word weer geshuffel.

### Gegroepeerde indeling
Indien daar 'n deelversameling (4 of minder diakens) van diakens is wat altyd saam op dieselfde Sondag ingedeel wil word, moet daar veranderinge op die `diakens.txt` gemaak word.

Die name van hierdie deelversameling moet langs mekaar in dieselfde lyn staan, en hulle moet geskei word met kommas.

Byvoorbeeld:
```
Jan,Piet,Wouter
```
