# Import necessary libraries
import os
import logging

os.makedirs("logs", exist_ok=True)

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,  # Log INFO and higher (WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs/app.log",  # Save logs in this file
    filemode="a"  # Append mode
)

# Create a logger instance
logger = logging.getLogger(__name__)
