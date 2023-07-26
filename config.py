import os
import dotenv

dotenv.load_dotenv()

DUNE_API_KEY = os.environ["DUNE_API_KEY"]
DUNE_DATA_CACHE_PATH = os.environ["DUNE_DATA_CACHE_PATH"]
LOG_FILE = os.environ["LOG_FILE"]


