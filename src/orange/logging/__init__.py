import logging

def paramlog(func):
    def interceptor(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug('%s: %s, %s', func.__name__, args, kwargs)
        return func(*args, **kwargs)
    return interceptor