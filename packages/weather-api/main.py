from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

OUTPUT_DIR = "../weather-scrapper/output"

@app.get("/csv")
async def download_csv():
    """
    Downloads Weather CSV file
    """
    file_path = os.path.join(OUTPUT_DIR, "weather_data.csv")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, filename="weather_data.csv", media_type="text/csv")

@app.get("/plot")
async def download_plot(name: str):
    """
    Downloads Weather Plot file using FileResponse.
    """
    if not os.path.exists(OUTPUT_DIR):
        raise HTTPException(status_code=404, detail="Output directory not found")
    
    valid_plots = [file.replace(".png", "") for file in os.listdir(OUTPUT_DIR) if file.endswith(".png")]
    if not valid_plots or len(valid_plots) == 0:
        raise HTTPException(status_code=404, detail="No valid plots found")

    if not name or name not in valid_plots:
        raise HTTPException(status_code=404, detail="Invalid plot name, Allowed plots: " + ', '.join(valid_plots))
    
    file_path = os.path.join(OUTPUT_DIR, f"{name}.png")
    return FileResponse(file_path, filename=f"{name}.png", media_type="image/png")