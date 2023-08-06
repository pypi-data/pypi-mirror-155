from functools import wraps
import logging
logger = logging.getLogger("pyhectiqlab")

def write_method(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.read_only:
            logger.error(f'Run is read only. Cannot execute `{f.__name__}`.')
            return
        return f(self, *args, **kwargs)
    return wrapper

def action_method(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.dry_mode:
            logger.error(f'`{f.__name__}` not executed. Dry (offline) mode.')
            return
        return f(self, *args, **kwargs)
    return wrapper

def beta(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        logger.warning('This method is still in development and can be unstable.')
        return f(self, *args, **kwargs)
    return wrapper

def will_be_depreciated(suggested_method):
    def _method(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            logger.warning(f'The method `{f.__name__}` will be removed in a future release. Use `{suggested_method}` instead.')
            return f(self, *args, **kwargs)
        return wrapper
    return _method