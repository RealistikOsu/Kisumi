from functools import cached_property
from typing import Optional
from logger import info, Ansi
import time

_TIME_SCALE = ( # (Unit string, minimum to use)
    ("s", 1e+9),
    ("ms", 1e+6),
    ("μs", 1e+3),
    ("ns", 0),
)

class Timer:
    """A nanosecond-precision timer class meant for high precision timing
    of specific code elements.
    
    Supports usage using `with` as

    ```py
    t = Timer()
    with t:
        # Code to time here.
        ...
    print(t.time_dif_ns)
    ```
    """

    def __init__(self) -> None:
        self._start = 0
        self._end = 0

    def start(self) -> None:
        """Begins the timer."""
        self._start = time.perf_counter_ns()
    
    def end(self) -> None:
        """Ends the timer, checking if it has been already started **after**
        setting the internal end value."""

        self._end = time.perf_counter_ns()
        assert self._start > 0

    # Context manager stuff.
    def __enter__(self) -> None:
        self.start()
    
    def __exit__(self) -> None:
        self.end()
    
    # Properties related to time differences.
    @cached_property
    def time_dif_ns(self) -> int:
        """Returns the time difference in nanoseconds."""

        return self._end - self._start
    
    @cached_property
    def time_dif_s(self) -> float:
        """Returns the time difference in seconds, rounded to 2dp."""

        return round(self.time_dif_ns / 1e+9, 2)
    
    @cached_property
    def time_dif_ms(self) -> float:
        """Returns the time difference in milliseconds, rounded to 2dp."""

        return round(self.time_dif_ns / 1e+6, 2)
    
    @cached_property
    def time_dif_us(self) -> float:
        """Returns the time difference in microseconds, rounded to 2dp."""

        return round(self.time_dif_ns / 1e+3, 2)
    
    @cached_property
    def time_dif_str(self) -> str:
        """Creates a string stating the difference in time, selecting the most
        appropriate unit and stating its short form."""

        for unit, min in _TIME_SCALE:
            if self.time_dif_ns > min:
                # FIXME: This is code repetition of the properties above. Currently
                # unable to thing of a way that allows us to use them without
                # triggering their execution.
                return f"{self.time_dif_ns / min:.2f}{unit}"
        # Sanity check.
        assert False, "Timer string generation exited the range of possible time?"

_TIME_COL = ( # (Unit string, minimum to use)
    ("ms", Ansi.GREEN),
    ("μs", Ansi.WHITE),
    ("ns", Ansi.WHITE),
    ("s", Ansi.YELLOW),
)

class PrintingPerfTimer(Timer):
    """A timer which directly prints its results to console if used using a
    `with` statement."""

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__()
        self._name = name
    
    # This is rather inefficient but shall rarely be used. We have to do
    # string based checks as we dont want data passed around in a weird manner.
    def __exit__(self, exc_type, *_) -> None:
        super().__exit__()

        mid_word = f"{Ansi.RED!r}failed in" if exc_type else "took"
        col = Ansi.WHITE
        # Determine the colour.
        for unit, colour in _TIME_COL:
            if self.time_dif_str.endswith(unit):
                col = colour
                break

        if self._name is not None:
            info(f"The execution of {self._name} {mid_word} {col!r}{self.time_dif_str}")
        else:
            info(f"Execution {mid_word} {col!r}{self.time_dif_str}")
