from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data")
GEODATA_PATH = BASE_DIR / os.getenv("GEODATA_PATH", "out/geodata.json")
LOCATIONS_PATH = BASE_DIR / os.getenv("LOCATIONS_PATH", "data/locations.csv")