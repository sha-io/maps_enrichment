from fastapi import FastAPI
from routes.geodata import router as polygon_router
from contextlib import asynccontextmanager
import geocode.geocode_utils as osm
import time
import os
import json
from config import LOCATIONS_PATH, GEODATA_PATH

async def load_geodata():
    if not os.path.exists(GEODATA_PATH):
        output = {}
        df = osm.get_filtered_dataset(LOCATIONS_PATH, "`Country/Region` == 'United Kingdom'")
        if df is not None:
            for _, rows in df.iterrows():
                lon = rows["Longitude"]
                lat = rows["Latitude"]
                data = osm.geocode_nominatim_boundary(lat, lon)
                time.sleep(1) # avoid rate limiting
                if type(data) is osm.Geodata:
                    bundle = {}
                    bundle["name"] = rows['Company Name']
                    bundle["entity_type"] = rows["Entity Type"]
                    bundle["geodata"] = data.model_dump()
                    output[data.osm_id] = bundle
            with open(GEODATA_PATH, "w") as geocode:
                json.dump(output, geocode, indent=4)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await load_geodata()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(polygon_router)
