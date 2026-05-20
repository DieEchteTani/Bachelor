from fastapi import FastAPI
import pandas as pd
import uvicorn

app = FastAPI()
FILE_NAME = "historisierung_poc.csv"

@app.get("/api/data")
def get_data_as_of(stichtag: str):
    """
    Nimmt einen Stichtag als Parameter an, filtert die CSV 
    und gibt die Daten als JSON zurück.
    """
    try:
        # Daten laden
        df = pd.read_csv(FILE_NAME)
        df['valid_from'] = pd.to_datetime(df['valid_from'])
        df['valid_to'] = pd.to_datetime(df['valid_to'])
        
        # Filterlogik anwenden
        target_date = pd.to_datetime(stichtag)
        mask = (df['valid_from'] <= target_date) & (df['valid_to'] >= target_date)
        result_df = df[mask].reset_index(drop=True)
        
        # Datumsfelder für den JSON-Export in Strings umwandeln
        result_df['valid_from'] = result_df['valid_from'].dt.strftime('%Y-%m-%d')
        result_df['valid_to'] = result_df['valid_to'].dt.strftime('%Y-%m-%d')
        
        # Rückgabe als Dictionary (wird automatisch in JSON konvertiert)
        return result_df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Startet den Server auf dem lokalen Rechner (127.0.0.1) auf Port 8000
    print("Starte Server auf http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)