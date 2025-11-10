import pandas as pd
import requests as fetch
from pydantic import BaseModel
from pathlib import Path

NOMINATIM_REVERSE_GEOCODING_URL = "https://nominatim.openstreetmap.org/reverse"


class RuntimeInfo(BaseModel):
    message: str

class Geodata(BaseModel):
    osm_id: int
    osm_type: str
    address: str
    country_code: str
    country: str
    bbox: list[float]
    geometry: dict

# Decorator to print out any custom messages returned by functions durring runtime
def logger(f):
    def get_runtime_info(*args):
        data = f(*args)
        if type(data) is RuntimeInfo:
            print(data.message)
        else:
            return data
    return get_runtime_info

def get_filtered_dataset(file: Path, filter: str) -> pd.DataFrame | None:
    try:
        df = pd.read_csv(file)
        df = df.query(filter)
        cols = ["Longitude", "Latitude", "Company Name"]
        for col in cols:
            df[col] = df[col].str.strip(" '")
        return df
    except Exception as e:
        print("An error occured:", e)

@logger
def geocode_nominatim_boundary(lat: float, lon: float) -> Geodata | RuntimeInfo :
    options = {
        "params": {
            "lat": lat,
            "lon": lon,
            "format": "geojson",
            "polygon_geojson": 1,
            "zoom": 18,
            "accept-language": "en",
        },
        "timeout": 5,
        "headers": {"User-Agent": "Nestle-Location-Intelligence-POC/1.0"},
    }
    try:
        r = fetch.get(NOMINATIM_REVERSE_GEOCODING_URL, **options)
        # Raise exception if HTTP request fails
        r.raise_for_status()
        data = r.json()

        if data:
            result = data.get("features", [None])[0]

            # Only proceed where there is any data to be processed
            if not result:
                raise ValueError("Error: No values found in data.")

            geometry = result.get("geometry", {})
            bbox = result.get("bbox", {})

            properties = result.get("properties", {})

            display_name = properties.get('display_name', '')
            address = properties.get('address', {})
            osm_id = properties.get("osm_id", "")
            osm_type = properties.get("osm_type", "")

            country = address.get('country', '')
            country_code = address.get('country_code', '')

            # Only use polygon data and no converting bbox to polygon, yet...
            if not geometry.get("type") == "Polygon":
                message = RuntimeInfo(message=f"Dropped:{geometry['type']}")
                return message

            return Geodata(osm_id=osm_id, osm_type=osm_type, address=display_name, country=country, country_code=country_code, bbox=bbox, geometry=geometry)

    except Exception as e:
        RuntimeInfo(message=f'An error has occured: , {e}')

    return RuntimeInfo(message="No Operation Performed.")
