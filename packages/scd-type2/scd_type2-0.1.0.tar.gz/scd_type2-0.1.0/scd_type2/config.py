import logging
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("scd_type2")

COLOURS = {
    "EOC": "\033[0m",  # End of colour
    "CYN": "\033[36m",  # Cyan
    "RED": "\033[91m",  # Red
    "MAG": "\033[35m",  # Magenta
}

today = date.today().strftime("%d/%m/%Y")
