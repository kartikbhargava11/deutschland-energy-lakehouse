import json
from pathlib import Path
from urllib.request import urlopen

# FILTER_ID und REGION sind fest: Last in Deutschland, 
FILTER_ID = 410
REGION = "DE" 

# dann liegt der Ordner immer am Repo-Root, egal woher du startest.
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "raw" / str(FILTER_ID)


# get_json ist nur der Download; ein helper funktion
def get_json(url):
     # Eine SMARD-URL öffnen und JSON zurückgeben
    with urlopen(url, timeout=60) as response:
        return json.load(response)

# main() baut den Ordner, liest timestamps, und schreibt jede Wochen-JSON nach data/raw/410/
def main():
    OUT.mkdir(parents=True, exist_ok=True) # Ordner anlegen, falls er fehlt

    # Datei 1: Inhaltsverzeichnis aller verfügbaren Wochen
    index_url = f"https://www.smard.de/app/chart_data/{FILTER_ID}/{REGION}/index_hour.json"

    # Nur die letzten 13 Wochen ≈ 90 Tage
    # [-13:] schneidet die Index-Liste auf die jüngsten 13 Wochen zu, damit es etwa 90 Tage sind, nicht die ganze Historie seit 2014.
    stamps = get_json(index_url)["timestamps"][-13:]


    for ts in stamps:
        # Datei 2: echte Stundenwerte für genau diese Woche
        url = (
            f"https://www.smard.de/app/chart_data/{FILTER_ID}/{REGION}/"
            f"{FILTER_ID}_{REGION}_hour_{ts}.json"
        )
        data = get_json(url)
        path = OUT / f"{FILTER_ID}_{REGION}_hour_{ts}.json"
        path.write_text(json.dumps(data))
        print("wrote", path.name, "hours", len(data.get("series", [])))

if __name__ == "__main__":
    main()