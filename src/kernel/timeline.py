"""Definition of main Timeline class.

This module defines the Timeline class, which provides an interface for the simulation kernel and drives event execution.
All entities are required to have an attached timeline for simulation.
"""

from _thread import start_new_thread
from math import inf
from sys import stdout
from time import time_ns, sleep
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .event import Event

from .eventlist import EventList


class Timeline:
    """ Class of timeline
    Timeline holds entities, which is configured before the simulation. Before the start of simulation, timeline must
    initialize all controlled entities. The initialization of entities may schedule events. The timeline pushes these
    events to its event list. The timeline starts simulation by popping the top event in the event list repeatedly. The
    time of popped event becomes current simulation time of timeline. The process of popped event is executed. The
    simulation stops if the timestamp on popped event is equal or larger than the stop time.

    To monitor the progress of simulation, people could change the value of Timeline.show_progress to show/hide progress
    bar.

    Args:
        stop_time (int): the stop time of simulation

    Attributes:
        events (EventList): the event list of timeline
        entities (List[Entity]): the entity list of timeline used for initialization
        time (int): current simulation time (picoseconds)
        stop_time (int): the stop (simulation) time of simulation
        show_progress (bool): show/hide the progress bar of simulation
        is_running (bool): if the simulation stops executing event
    """

    def __init__(self, stop_time=inf):
        self.events = EventList()
        self.entities = []
        self.time = 0
        self.stop_time = stop_time
        self.event_counter = 0
        self.show_progress = False
        self.is_running = False

    def now(self) -> int:
        return self.time

    def schedule(self, event: "Event") -> None:
        self.event_counter += 1
        return self.events.push(event)

    def init(self) -> None:
        for entity in self.entities:
            entity.init()

    def run(self) -> None:
        self.is_running = True

        if self.show_progress:
            self.progress_bar()

        # log = {}
        while len(self.events) > 0:
            event = self.events.pop()
            if event.time >= self.stop_time:
                self.schedule(event)
                break
            assert self.time <= event.time, "invalid event time for process scheduled on " + str(event.process.owner)
            self.time = event.time
            # if not event.process.activation in log:
            #     log[event.process.activation] = 0
            # log[event.process.activation]+=1
            event.process.run()

        # print('number of event', self.event_counter)
        # print('log:',log)

        self.is_running = False

    def stop(self) -> None:
        self.stop_time = self.now()

    def remove_event(self, event: "Event") -> None:
        self.events.remove(event)

    def update_event_time(self, event: "Event", time: int) -> None:
        self.events.remove(event)
        event.time = time
        self.schedule(event)

    def seed(self, seed: int) -> None:
        from numpy import random
        random.seed(seed)

    def progress_bar(self):
        def print_time():
            start_time = time_ns()
            while self.is_running:
                exe_time = self.ns_to_human_time(time_ns() - start_time)
                sim_time = self.ns_to_human_time(self.time / 1e3)
                if self.stop_time == float('inf'):
                    stop_time = 'NaN'
                else:
                    stop_time = self.ns_to_human_time(self.stop_time / 1e3)
                process_bar = f'\rexecution time: {exe_time};     simulation time: {sim_time} / {stop_time}'
                print(f'{process_bar}', end="\r")
                stdout.flush()
                sleep(3)

        start_new_thread(print_time, ())

    def ns_to_human_time(self, nanosec: int) -> str:
        if nanosec >= 1e6:
            ms = nanosec / 1e6
            nanosec = nanosec % 1e6
            if ms >= 1e3:
                second = ms / 1e3
                if second >= 60:
                    minute = second // 60
                    second = second % 60
                    if minute >= 60:
                        hour = minute // 60
                        minute = minute % 60
                        return '%d hour: %d min: %.2f sec' % (hour, minute, second)
                    return '%d min: %.2f sec' % (minute, second)
                return '%.2f sec' % (second)
            return "%d ms, %.2f ns" % (ms, nanosec)
        return '%d ns' % nanosec
