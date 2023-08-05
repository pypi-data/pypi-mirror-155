#!/bin/python3

import logging
import os

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=os.environ.get("LOGLEVEL", "INFO"),
)
