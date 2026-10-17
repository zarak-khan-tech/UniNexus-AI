# English: Reliability utilities — timeout wrappers for synchronous calls.
# Roman Urdu: Reliability utilities — synchronous calls ke liye timeout wrappers.

import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from typing import Callable, Any

logger = logging.getLogger(__name__)

def run_with_timeout(fn: Callable[..., Any], timeout_sec: float, *args, **kwargs) -> Any:
    """
    English: Run a synchronous function with a timeout. Raises TimeoutError if it exceeds the limit.
    Roman Urdu: Ek synchronous function ko timeout ke saath chalao. Agar limit cross ho to TimeoutError raise karo.
    """
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(fn, *args, **kwargs)
        try:
            return future.result(timeout=timeout_sec)
        except FutureTimeoutError:
            logger.warning(f"Execution of {getattr(fn, '__name__', 'function')} timed out after {timeout_sec}s")
            raise TimeoutError(f"Function timed out after {timeout_sec} seconds.")
