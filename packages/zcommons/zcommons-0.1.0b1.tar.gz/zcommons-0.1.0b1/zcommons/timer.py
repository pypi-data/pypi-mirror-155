__all__ = [
    "Timer",
    "timer"
]

from functools import wraps
from typing import Union, List, Dict, Tuple

from .units import TimeUnits
from . import time as time


class Timer(object):
    """
    A Single Thread Timer
    =====================
    A timer which supports start, pause, record, etc.
    """

    def __init__(self, name: str = "Timer", unit: Union[str, TimeUnits] = TimeUnits.SECOND):
        """

        :param name: a meaningful string representing the timer function.
        :param unit: the unit of result.
        """
        super(Timer, self).__init__()
        self.name = name
        self.unit = TimeUnits(unit)
        self.__records = []
        self.__elapsed_time_ns = [0, 0]
        self.__record_time_ns = [0, 0]
        self.__start_time_point_ns = [0, 0]
        self.__stop_time_point_ns = [0, 0]
        self.__running = False
        self.__pausing = False

    def start(self) -> None:
        """
        Start the timer.
        There will have no effect if the timer already started.

        :return:
        """
        if self.__running:
            return
        self.__running = True
        self.__start_time_point_ns = time.perf_counter_ns(), time.process_time_ns()

    def pause(self) -> None:
        """
        Pause the timer.
        There will have no effect if the timer not in running or already paused.

        :return:
        """
        if not self.__running or self.__pausing:
            return
        self.__pausing = True
        pc, pt = time.perf_counter_ns(), time.process_time_ns()
        self.__record_time_ns[0] += pc - self.__start_time_point_ns[0]
        self.__record_time_ns[1] += pt - self.__start_time_point_ns[1]

    def resume(self) -> None:
        """
        Resume the timer from pausing status.
        There will have no effect if the timer not in running or not in pausing.

        :return:
        """
        if not self.__running or not self.__pausing:
            return
        self.__start_time_point_ns = [time.perf_counter_ns(), time.process_time_ns()]
        self.__pausing = False

    def record(self) -> None:
        """
        Generate a new time record.
        There will have no effect if the timer not in running.

        :return:
        """
        self.__record(is_stop=False)

    def stop(self) -> None:
        """
        Stop the timer and generate a new time record.
        There will have no effect if the timer not in running.

        :return:
        """
        self.__record(is_stop=True)
        self.__running = False

    def elapsed_records(self, unit: Union[str, TimeUnits] = None, exclude_zero: bool = False) -> List[Dict[str, int]]:
        """
        Get all records with specified unit.

        :param unit: the time unit of result, the ``self.unit`` will be used if it is ``None``.
        :param exclude_zero:  whether ignore the records which have zero time duration. If call ``record`` repeatly in
        pausing status, zero time duration records will be generated.
        :return: a record list.
        """
        if unit is None:
            unit = self.unit
        ret = []
        for r in self.__records:
            if exclude_zero and r[0] == 0 and r[1] == 0:
                continue
            ret.append({
                "perf_counter": TimeUnits.NANO.convert_to(r[0], unit),
                "process_time": TimeUnits.NANO.convert_to(r[1], unit)
            })
        return ret

    def last_record(self, unit: Union[str, TimeUnits] = None, exclude_zero: bool = False) -> Tuple[int, int]:
        """
        The elapsed time from last record with ``unit``.

        :param unit: the time unit of result, the ``self.unit`` will be used if it is ``None``.
        :param exclude_zero: whether ignore the records which have zero time duration.
        :return:
        """
        if unit is None:
            unit = self.unit
        pc_ns, pt_ns = self.last_record_ns(exclude_zero)
        pc = TimeUnits.NANO.convert_to(pc_ns, unit)
        pt = TimeUnits.NANO.convert_to(pt_ns, unit)
        return pc, pt

    def last_record_ns(self, exclude_zero: bool = False) -> Tuple[int, int]:
        """
        The elapsed nanoseconds from last record.

        :param exclude_zero: whether ignore the records which have zero time duration.
        :return:
        """
        if not self.__running:
            for i in range(len(self.__records) - 1, -1, -1):
                if not exclude_zero or (self.__records[i][0] == 0 and self.__records[i][1] == 0):
                    return tuple(self.__records[i])
            return 0, 0
        else:
            if self.__pausing:
                return self.__record_time_ns[0], self.__record_time_ns[1]
            else:
                pc, pt = time.perf_counter_ns(), time.process_time_ns()
                return self.__record_time_ns[0] + pc - self.__start_time_point_ns[0], \
                       self.__record_time_ns[1] + pt - self.__start_time_point_ns[1]

    def elapsed(self, unit: Union[str, TimeUnits] = None) -> Tuple[int, int]:
        """
        The elapsed time from started time point with ``unit``.
        If the timer already stopped, this method will return the duration from started to stopped time point.

        :param unit: the time unit, the ``self.unit`` will be used if it is ``None``.
        :return: a tuple of perf counter and process time
        """
        if unit is None:
            unit = self.unit
        pc_ns, pt_ns = self.elapsed_ns()
        pc = TimeUnits.NANO.convert_to(pc_ns, unit)
        pt = TimeUnits.NANO.convert_to(pt_ns, unit)
        return pc, pt

    def elapsed_ns(self) -> Tuple[int, int]:
        """
        The elapsed nanoseconds from started time point.
        If the timer already stopped, this method will return the duration from started to stopped time point.

        :return: a tuple of perf counter and process time
        """
        if not self.__running:
            return self.__elapsed_time_ns[0], self.__elapsed_time_ns[1]
        else:
            rec_pc, rec_pt = self.__record_elapsed()
            return self.__elapsed_time_ns[0] + rec_pc, self.__elapsed_time_ns[1] + rec_pt

    def __record(self, is_stop=False):
        if not self.__running:
            return
        rec_pc, rec_pt = self.__record_elapsed(is_stop=is_stop)
        self.__records.append((rec_pc, rec_pt))
        self.__record_time_ns = [0, 0]
        self.__elapsed_time_ns[0] += rec_pc
        self.__elapsed_time_ns[1] += rec_pt

    def __record_elapsed(self, is_stop=False):
        rec_pc, rec_pt = self.__record_time_ns
        pc, pt = time.perf_counter_ns(), time.process_time_ns()
        if not self.__pausing:
            rec_pc += pc - self.__start_time_point_ns[0]
            rec_pt += pt - self.__start_time_point_ns[1]
        self.__start_time_point_ns = [pc, pt]
        if is_stop:
            self.__stop_time_point_ns = [pc, pt]
        return rec_pc, rec_pt

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def __show_timer_res(res: dict):
    print(f"Run {res['name']} for {res['repeat']} times.")
    print(f"  |- Total perf counter: {res['perf_counter']}{res['unit']}")
    print(f"  |- Total process time: {res['process_time']}{res['unit']}")
    print(f"  |- Avg   perf counter: {res['perf_counter'] / res['repeat']}{res['unit']}")
    print(f"  |- Avg   process time: {res['process_time'] / res['repeat']}{res['unit']}")
    print()
    print(f"The following is a detailed time record of each run:")

    def __left_pad_zero(x: int, ndigits: int):
        x_str = str(x)
        zero_str = "0" * (ndigits - len(x_str))
        return zero_str + x_str

    if res['repeat'] <= 10:
        for i in range(res["repeat"]):
            print(f"Run {i + 1:02} - perf counter: {res['records'][i]['perf_counter']}{res['unit']}")
            print(f"       - process time: {res['records'][i]['process_time']}{res['unit']}")
    else:
        ndigits = len(str(res["repeat"]))
        for i in range(5):
            print(
                f"Run {__left_pad_zero(i + 1, ndigits)} - perf counter: {res['records'][i]['perf_counter']}{res['unit']}")
            print(f"    {' ' * ndigits} - process time: {res['records'][i]['process_time']}{res['unit']}")
        print(f"....{'.' * ndigits}")
        for i in range(res["repeat"] - 5, res["repeat"]):
            print(
                f"Run {__left_pad_zero(i + 1, ndigits)} - perf counter: {res['records'][i]['perf_counter']}{res['unit']}")
            print(f"    {' ' * ndigits} - process time: {res['records'][i]['process_time']}{res['unit']}")


def timer(name: str = None, unit: Union[str, TimeUnits] = TimeUnits.SECOND, repeat: int = 1, res: dict = None,
          show: bool = False):
    """
    the decorator of Timer.

    :param name: the timer task name
    :param unit: the unit of res
    :param repeat: exec task function times
    :param res: a dict for storing result
    :param show: whether print timer info to stdout
    :return: the first exec result of task func
    """

    def decorate(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            real_name = name
            if real_name is None:
                real_name = getattr(func, "__name__", None)
            if real_name is None:
                real_name = "timer"
            real_res = res
            if real_res is None:
                real_res = {}

            with Timer(real_name, unit) as tmer:
                ret = func(*args, **kwargs)
                if repeat > 1:
                    for _ in range(repeat - 1):
                        tmer.record()
                        func(*args, **kwargs)

            pc, pt = tmer.elapsed()
            real_res["name"] = real_name
            real_res["unit"] = TimeUnits(unit).value
            real_res["repeat"] = repeat
            real_res["perf_counter"] = pc
            real_res["process_time"] = pt
            real_res["records"] = tmer.elapsed_records()
            if show:
                __show_timer_res(real_res)

            return ret

        return wrapper

    return decorate
