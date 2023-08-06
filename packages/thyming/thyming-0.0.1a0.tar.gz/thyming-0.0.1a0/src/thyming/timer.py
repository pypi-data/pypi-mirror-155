from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime as dt
from enum import Enum
import logging
from time import perf_counter, sleep
from typing import Callable, Literal, Union

@dataclass
class AbstractTimerError(Exception, ABC):
    timer_name: str
    timestamp: dt
    message: str = field(init=False)
    @abstractmethod
    def __post_init__(self) -> None:
        ...

class TimerAlreadyRunningError(AbstractTimerError):
    def __post_init__(self) -> None:
        self.message = f'[{self.timestamp.isoformat()}] Tried to start {self.timer_name} but it was already running.'

MeasureOrStop = Literal['measure', 'stop']
@dataclass
class TimerNotRunningError(AbstractTimerError):
    action: MeasureOrStop
    def __post_init__(self) -> None:
        self.message = f'[{self.timestamp.isoformat()}] Tried to click `{self.action}` on {self.timer_name} but it wasn\'t running.'

@dataclass
class NoLoggerError(AbstractTimerError):
    logger_message: TimerMessage
    def __post_init__(self) -> None:
        self.message = f'[{self.timestamp.isoformat()}] Message `{self.logger_message}` was passed to logger but {self.timer_name} has no logger'

class Timestamp(Enum):
    START   = 0
    MEASURED= 1
    END     = 2

TimerMessage = Union[str, None, Timestamp]

@dataclass
class Timer:
    name: Union[str, None] = None
    message: str = "Elapsed time: {:0.4f} seconds."
    logger: Union[Callable[[str], None], None] = field(default=logging.info)
    start_time: Union[float, None] = field(default=None, repr=False)
    recorded_times: list[float] = field(default_factory=list, init=False, repr=False)

    @staticmethod
    def _timestamp_to_msg(timestamp: Timestamp) -> str:
        if timestamp == Timestamp.START:
            return f'START: {dt.now().isoformat("T","seconds")}'
        if timestamp == Timestamp.MEASURED:
            return f'MEASURED: {dt.now().isoformat("T","seconds")}'
        if timestamp == Timestamp.END:
            return f'END: {dt.now().isoformat("T","seconds")}'
    
    def start(self, click_message: TimerMessage=None) -> Timer: #TODO: after upgrading to 3.11, change to typing.Self
        if self.start_time is not None:
            raise TimerAlreadyRunningError(self._timer_name, dt.now())
        self.start_time = perf_counter()
        if click_message:
            if self.logger is None:
                raise NoLoggerError(self._timer_name, dt.now(), click_message)
            self.log(click_message)
        return self

    @property
    def _timer_name(self) -> str:
        return 'timer {self.name if self.name else ""}'.replace('  ', ' ')

    def _get_logging_message(self, *, 
                             recorded_time: float, 
                             click_message_pre: TimerMessage,
                             click_message_post: TimerMessage) -> str:
        if isinstance(click_message_pre, Timestamp):
            click_message_pre = Timer._timestamp_to_msg(click_message_pre)
        if isinstance(click_message_post, Timestamp):
            click_message_post = Timer._timestamp_to_msg(click_message_post)
        if click_message_pre:
            msg = f'{click_message_pre}\n'
        elif self.name:
            msg = f'{self.name}:\n'
        else:
            msg = ''
        msg += self.message.format(recorded_time)
        if click_message_post:
            msg += '\n' + click_message_post
        return msg
        
    def _click(self, *, stop_timer: bool, click_message_pre: TimerMessage, click_message_post: TimerMessage, action: MeasureOrStop) -> float:
        if self.start_time is None:
                raise TimerNotRunningError(self._timer_name, dt.now(), action)
        recorded_time = perf_counter() - self.start_time
        if stop_timer:
            self.start_time = None
        self.recorded_times.append(recorded_time)
        if self.logger:
            self.log(self._get_logging_message(recorded_time=recorded_time, click_message_pre=click_message_pre, click_message_post=click_message_post))
        return recorded_time

    def stop(self, click_message_pre: TimerMessage=None, click_message_post: TimerMessage=None) -> float:
        return self._click(stop_timer=True, click_message_pre=click_message_pre, click_message_post=click_message_post, action='stop')
        
    def measure(self, click_message_pre: TimerMessage=None, click_message_post: TimerMessage=None) -> float:
        return self._click(stop_timer=False, click_message_pre=click_message_pre, click_message_post=click_message_post, action='measure')

    def log(self, msg: TimerMessage) -> Timer:
        if self.logger is None:
            raise NoLoggerError(self._timer_name, dt.now(), msg)
        if msg is None:
            return self
        if isinstance(msg, Timestamp):
            self.logger(Timer._timestamp_to_msg(msg))
            return self
        for msg_line in msg.split('\n'):
            self.logger(msg_line)
        return self
    
    @property
    def times(self) -> list[float]:
        return self.recorded_times

    def __enter__(self) -> None:
        self.start()

    def __exit__(self) -> None:
        if self.start_time is not None:
            self.stop()

    def restart(self, 
                click_message_pre: TimerMessage, 
                click_message_post: TimerMessage) -> Timer:
        self.stop(click_message_pre, click_message_post)
        return self.start()

    def sleep(self, secs: float) -> None:
        sleep(secs)
