import logging
import re
import requests
from typing import Collection

logger = logging.getLogger(__name__)

def check_urls(urls: Collection[str], timeout: int) -> dict[str, str]:
    """
    Check a list of URLs and return status.

    Args:
        urls: A list of URL strings to check.
        timeout: Maximum time in seconds to wait for each request.
    
    Returns:
        A dictionary mapping each URL to its status.
    """

    logger.info(f"Starting check for {len(urls)} URLs with a timeout {timeout}")
    results = {}

    for url in urls:
        status = "UNKNOWN"

        try:
            logger.debug(f"Checking URL: {url}")
            response = requests.get(url, timeout=timeout)

            if response.ok:
                status = f"{response.status_code}_OK"
        except requests.exceptions.Timeout:
            status = "TIMEOUT"
            logger.warning(f"Request to {url} timed out.")
        except requests.exceptions.ConnectionError:
            status = "CONNECTION_ERROR"
            logger.warning(f"Connection error for {url}.")
        except requests.exceptions.RequestException as e:
            status = f"REQUEST_ERROR: {type(e).__name__}"
            logger.error(f"Request exception for {url} {e}.")

        results[url] = status
        logger.debug(f"Checked: {url:<40} -> {status}")
    logger.info("Completed URL checks.")
    return results
