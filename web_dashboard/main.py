from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import pandas as pd
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

CSV_FILE = "logs/2025-09-12.csv"
WEATHER_FILE = "dataset/cordoba_weather_aug_2025.csv"


def preprocess(df):
    df = df.resample("1s").ffill()

    # Compute derived metrics
    df["energy_kWh"] = df["power"] / 3600000
    df["total_kWh"] = df["energy_kWh"].sum()
    df["cumulative_kWh"] = df["energy_kWh"].cumsum()
    df["status"] = df["power"] != 0

    # Group ON/OFF segments
    df["group"] = (df["status"] != df["status"].shift()).cumsum()
    grouped = df.groupby("group").agg({"status": "first"})

    # Calculate the full duration of each segment
    grouped["duration"] = df.groupby("group").apply(
        lambda g: (g.index[-1] - g.index[0]).seconds / 60,
        include_groups=False)

    # Calculate the middle time of each segment to add labels to the plot later
    grouped["mid_time"] = df.groupby("group").apply(
        lambda g: g.index[len(g) // 2],
        include_groups=False)

    # Map durations and mid_times back to original df
    df["duration"] = df["group"].map(grouped["duration"])
    df["mid_time"] = df["group"].map(grouped["mid_time"])
    return df


def get_segments(df):
    grouped = df.groupby("group").agg({
        "status": "first",
        "mid_time": "first",
        "duration": "first",
    })
    # Add start/end for plotting steps
    df_segments = df.groupby("group").agg(start=("timestamp", "first"),
                end=("timestamp", "last"), status=("status", "first"),
                duration=("duration", "first"),
                mid_time=("mid_time", "first"))
    df_segments = df_segments.reset_index(drop=True)
    # Convert timestamps to strings
    df_segments["start"] = df_segments["start"].astype(str)
    df_segments["end"] = df_segments["end"].astype(str)
    df_segments["mid_time"] = df_segments["mid_time"].astype(str)
    return df_segments


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/init-data")
async def init_data():
    df = pd.read_csv(CSV_FILE, parse_dates=["timestamp"],
                     index_col="timestamp")
    df = preprocess(df)
    df = df.reset_index()
    df["timestamp"] = df["timestamp"].astype(str)
    df["mid_time"] = df["mid_time"].astype(str)

    segments_df = get_segments(df)
    segments = segments_df.to_dict(orient="records")
    return JSONResponse(content={
        "data": df.to_dict(orient="records"),
        "segments": segments
    })


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
