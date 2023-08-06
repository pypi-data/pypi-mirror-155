# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import datetime as dt
import logging
import os
import threading

from apm_client.core.agent.commands import ApplicationEvent
from apm_client.core.agent.socket import CoreAgentSocketThread
from apm_client.core.samplers.cpu import Cpu
from apm_client.core.samplers.memory import Memory
from apm_client.core.threading import SingletonThread

logger = logging.getLogger(__name__)


class SamplersThread(SingletonThread):
    _instance_lock = threading.Lock()
    _stop_event = threading.Event()

    def run(self):
        logger.debug("Starting Samplers.")
        instances = [Cpu(), Memory()]

        while True:
            # from utils.log import celery_print
            # celery_print('10')
            for instance in instances:
                event_value = instance.run()
                if event_value is not None:
                    event_type = instance.metric_type + "/" + instance.metric_name
                    event = ApplicationEvent(
                        event_value=event_value,
                        event_type=event_type,
                        timestamp=dt.datetime.utcnow(),
                        source="Pid: " + str(os.getpid()),
                    )
                    # send_to_me(f'In sampler thread: \n{event.message()}')
                    CoreAgentSocketThread.send(event)

            should_stop = self._stop_event.wait(timeout=60)
            if should_stop:
                logger.debug("Stopping Samplers.")
                break
