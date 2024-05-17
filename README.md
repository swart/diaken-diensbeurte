# Diaken Diensbeurte

Hierdie program skep diaken diensbeurte in 'n totaal lukrake en regverdige manier.

Die inset is 'n lys diakens (`./diakens.txt`) en die uitset is 'n paar PDF en CSV lêers (`./data/x.pdf` en `./data/x.csv`).

## Stel omgewing op
Hardloop die volgende instruksies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Hoe om te gebruik?
Doen gewoon `python main.py`. Dit sal diaken diensbeurte vir die volgende 6 maande uitwerk.

Daar is opsies beskikbaar wat u sal toelaat om die hoeveelheid maande en indelingstrategie te kies. Vir meer inligting sien `python main.py --help`.

'n Opsomming van die opsies:
- -m, --maande: Hoeveelheid maande om die diensbeurte uit te werk.
    - Verstekwaarde is 6.
- -s, --strategie: Strategie vir indeling.
    - 1: Shuffle en deel diakens in elke sondag.
    - 2: Shuffle die hele diakenlys elke siklus.

## Hoe werk die indeling?
Die hele diakenlys word eenmaal geshuffel (volgens die [Fisher-Yates algoritme](https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle)), daarna word die name sekwensieel in groepe van 4 per Sondag ingedeel. Elke Sondag se 4 name word weer geshuffel.
