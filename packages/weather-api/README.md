# Singular - Weather Data Api

- [Overview](#overview)
- [Instructions](#instructions)
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Usage](#usage)

## Overview

This is a Python FastAPI application that allows the user to download the weather data and plots from the Singular - Weather Data Scrapper application.

## Instructions

### Requirements
- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/)
- [FastAPI](https://fastapi.tiangolo.com/)

### Setup
1. Sync the project dependencies by running the following command in the root directory of the project:
```bash
uv sync
```

2. Go to project directory by running the following command:
```bash
cd /packages/weather-api
```

### Usage

1. Run the application by running the following command:
```bash
uv run fastapi dev
```

The application will be available at http://127.0.0.1:8000

2. To download the weather data, you can use the following URL:
```
http://127.0.0.1:8000/csv
```


3. To download a plot, you can use the following URL:
```
http://127.0.0.1:8000/plot?name={PLOT_FILE_NAME}
```

Replace `PLOT_FILE_NAME` with the name of the plot file you want to download. If the plot file is not found, the API will return a 404 error.

Make sure `output` directory is present in Weather Data Scrapper project directory. If not, the api will return a 404 error.