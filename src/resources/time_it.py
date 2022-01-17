import functools
from datetime import datetime
from time import perf_counter

MSG = '[DETAIL] {0} {1}, time consumed: {2:.6f} ms'


def ct() -> str:
    return datetime.now().isoformat()


def time_it(method):

    @functools.wraps(method)
    def timed(*args, **kw):
        result = None
        start_time = perf_counter()
        try:
            result = method(*args, **kw)
        except Exception as exc:
            exception = exc
            raise exc from None
        finally:
            end_time = perf_counter()
            result_time = (end_time - start_time) * 1000
            print(MSG.format(ct(), method.__name__, result_time))
        return result

    return timed
