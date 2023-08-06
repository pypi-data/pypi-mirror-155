import hashlib
import json
import time
import logging


metabase_io_log = logging.getLogger("metabase.io")

def api_collection_id(collection_id):
    return collection_id if collection_id != "root" else None


def uuid(item):
    """
    Returns an UUID that is a function of item id.
    """
    return hashlib.md5(str(item["id"]).encode()).hexdigest()


def content_hash(item):
    return hashlib.md5(json.dumps(item, sort_keys=True).encode()).hexdigest()

def get_in(dictionary, key_list):
    p = dictionary
    found = True
    for a in key_list:
        if a in p:
            p = p[a]
        else:
            found = False
    if found:
        return p


def retry(retry_count=3, retry_interval=5):
    """
    Retry decorator

    Example:
    @retry(3, 2) or @retry()
    def test():
      pass
    """
    def real_decorator(decor_method):
        def wrapper(*args, **kwargs):
            for count in range(retry_count):
                try:
                    return_values = decor_method(*args, **kwargs)
                    return return_values
                except Exception as error:
                    # On exception, retry till retry_frequency is exhausted
                    metabase_io_log.fatal("retry: %s . Function execution failed for %s" %
                                 (count + 1, decor_method.__name__))
                    # sleep for retry_interval
                    time.sleep(retry_interval)
                    # If the retries are exhausted, raise the exception
                    if count == retry_count-1:
                        raise error
        return wrapper
    return real_decorator
