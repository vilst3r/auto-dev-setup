"""
Setup the logger for the automation script
"""

# Native Modules
import logging

LOGGER = logging.getLogger()


def initialise_logger():
    """
	Set up logging for writing stdout & stderr to files
	"""
    LOGGER.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    out_path = "logs/setup_out.log"
    err_path = "logs/setup_err.log"

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    out_handler = logging.FileHandler(f"{out_path}", "w+")
    out_handler.setLevel(logging.DEBUG)
    out_handler.setFormatter(formatter)

    err_handler = logging.FileHandler(f"{err_path}", "w+")
    err_handler.setLevel(logging.WARNING)
    err_handler.setFormatter(formatter)

    LOGGER.addHandler(out_handler)
    LOGGER.addHandler(err_handler)
    LOGGER.addHandler(stream_handler)
