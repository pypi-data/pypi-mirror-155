import logging
import sys


from .server.server import run_server
from LigralPy.config import get_workdir, set_workdir

logger = logging.getLogger(__name__)
try:
    logger.warning(f"Current work directory is: {get_workdir()}")
except FileNotFoundError:
    logger.warning(f"Current work directory is Undefined!")
run_server()
