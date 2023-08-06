from __future__ import annotations

import time
from typing import Any, Callable

import rich


def trace_time(method: Callable):
    def timed(*args: Any, **kwargs: Any):
        start_time = time.time()
        result = method(*args, **kwargs)
        runtime = int((time.time() - start_time) * 1000)
        if "log_time" in kwargs:
            name = kwargs.get("log_name", method.__name__.upper())
            kwargs["log_time"][name] = runtime
        else:
            rich.print(f"{method.__name__} took {runtime} ms")
        return result

    return timed


if __name__ == "__main__":

    @trace_time
    def func(a, b):
        for _ in range(int(1e6)):
            _ = a + b
        return a + b

    func(1, b=2)
