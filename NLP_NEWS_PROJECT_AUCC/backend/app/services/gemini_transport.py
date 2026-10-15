"""Bounded retries for temporary upstream failures, without logging payloads or keys."""
import logging
import time

import httpx

logger = logging.getLogger(__name__)
TRANSIENT_STATUSES = {500, 502, 503, 504}


def post_with_retry(url, *, headers, json, timeout, client=None):
    post = client.post if client is not None else httpx.post
    deadline = time.monotonic() + timeout
    for attempt in range(3):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise httpx.ReadTimeout("Gemini request deadline exceeded")
        response = post(url, headers=headers, json=json, timeout=remaining)
        if response.status_code not in TRANSIENT_STATUSES:
            return response
        logger.warning("Gemini upstream HTTP %d, attempt %d/3", response.status_code, attempt + 1)
        delay = 2 ** attempt
        if attempt == 2 or deadline - time.monotonic() <= delay:
            return response
        time.sleep(delay)
