import secrets
import signal
import json
import logging
import struct
import socket
import threading
import time
import sched
from datetime import datetime
from datetime import timedelta

import requests
import traceback
import os
from enum import Enum


# class SingletonThread(threading.Thread):
#     _instance = None
#
#     @classmethod
#     def ensure_started(cls):
#         instance = cls._instance
#         if instance is not None and instance.is_alive():
#             # No need to grab the lock
#             return
#         with cls._instance_lock:
#             if cls._instance is None or not cls._instance.is_alive():
#                 cls._instance = cls()
#                 cls._instance.start()
#
#     @classmethod
#     def ensure_stopped(cls):
#         if cls._instance is None:
#             # No need to grab the lock
#             return
#         with cls._instance_lock:
#             if cls._instance is None:
#                 # Nothing to stop
#                 return
#             elif not cls._instance.is_alive():
#                 # Thread died
#                 cls._instance = None
#                 return
#
#             # Signal stopping
#             cls._stop_event.set()
#             cls._on_stop()
#             cls._instance.join()
#
#             cls._instance = None
#             cls._stop_event.clear()
#             # print('Stop event cleared')
#
#     @classmethod
#     def _on_stop(cls):
#         """
#         Hook to allow subclasses to add extra behaviour to stopping.
#         """
#         pass
#
#     def __init__(self, *args, **kwargs):
#         super(SingletonThread, self).__init__(*args, **kwargs)
#         self.daemon = True
#


class ReportType(Enum):
    Endpoint = 0
    Task = 1
    OtherCommands = 2
    Register = 3


class BatchCommandType(Enum):
    Endpoint = 0
    Task = 1


server_address = 'https://apm.tabdealbot.com/batch_report/'
my_bot = 'https://sadeghiaa.pythonanywhere.com'
logger = logging.getLogger(__name__)


def farewell(signum, frame):
    logger.debug('farewell')
    requests.post(my_bot, 'farewell')
    CoreAgent.sock.close()
    time.sleep(1)
    return


def send_to_server(s, content_type):
    try:
        if content_type in [ReportType.Task.value, ReportType.Endpoint.value]:
            result = requests.post(server_address, json=s)
        elif content_type == ReportType.Register.value:
            result = requests.put(server_address, json=s)
        else:
            return False

        if result.status_code != 200:
            log_error(f"{result.status_code}")
        return result.status_code == 200
    except:
        log_error(f'In send_to_server\n{traceback.format_exc()}')
        return False


def log_error(s):
    with open('apm_log.txt', 'a') as f:
        f.write(f'{datetime.now()} PID: {os.getpid()} {os.path.dirname(os.path.realpath(__file__))}\n{s}\n\n')


def timedelta_to_us(response_time):
    us_time = 0
    if response_time.days != 0:
        us_time += 86400000000 * response_time.days
    if response_time.seconds != 0:
        us_time += 1000000 * response_time.seconds
    us_time += response_time.microseconds
    return us_time


def is_template(name):
    return name.startswith('Template') or name.startswith('Block')


def get_span_name(span_name):
    if span_name.startswith('SQL'):
        return 'SQL'
    elif span_name.startswith('Controller'):
        return 'View'
    elif span_name.startswith('Redis'):
        return 'Redis'
    elif span_name.startswith('HTTP'):
        return 'HTTP'
    elif span_name.startswith('Template') or span_name.startswith('Block'):
        return 'Rendering'
    elif span_name.startswith('Middleware'):
        return 'Middleware'
    elif span_name.startswith('Job'):
        return 'Python'
    else:
        return 'Custom'


class Span:
    def __init__(self, span_id, span_name, elapsed_time):
        self.span_id = span_id
        self.span_name = span_name
        self.elapsed_time = elapsed_time
        self.children = []

    def __str__(self):
        return self.span_name

    def __getstate__(self):
        return {'span_id': self.span_id,
                'operation': self.span_name,
                'elapsed_time': self.elapsed_time,
                'children': self.children}


class Spans:
    def __init__(self):
        self.Custom = Span(elapsed_time=0, span_id=None, span_name=None)
        self.HTTP = Span(elapsed_time=0, span_id=None, span_name=None)
        self.Middleware = Span(elapsed_time=0, span_id=None, span_name=None)
        self.Redis = Span(elapsed_time=0, span_id=None, span_name=None)
        self.SQL = Span(elapsed_time=0, span_id=None, span_name=None)
        self.View = Span(elapsed_time=0, span_id=None, span_name=None)
        self.Rendering = Span(elapsed_time=0, span_id=None, span_name=None)
        self.Python = Span(elapsed_time=0, span_id=None, span_name=None)

    def get_dict(self):
        return {k: {"elapsed_time": v.elapsed_time} for k, v in vars(self).items()}


class AggregateOperationSummary:
    def __init__(self, num_operations=0, sum_elapsed_time=0.0, spans=None):
        self.num_operations = num_operations
        self.sum_elapsed_time = sum_elapsed_time
        self.spans = spans if spans is not None else AggregatedSpans()

    def get_dict(self):
        return {
            "num_operations": self.num_operations,
            "sum_elapsed_time": self.sum_elapsed_time,
            "spans": self.spans.get_dict()
        }

    def get_mixed_with(self, other):
        return AggregateOperationSummary(
            num_operations=self.num_operations + other.num_operations,
            sum_elapsed_time=self.sum_elapsed_time + other.sum_elapsed_time,
            spans=self.spans.get_mixed_with(other.spans)
        )


class OperationInfo:
    def __init__(self, elapsed_time, start_time, operation_name, operation_type, spans: Spans):
        self.elapsed_time = elapsed_time
        self.start_time: datetime = start_time
        self.operation_name = operation_name
        self.operation_type = operation_type
        self.spans = spans

    def get_dict(self):
        return {
            "elapsed_time": self.elapsed_time,
            "start_time": self.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "operation_name": self.operation_name,
            "operation_type": self.operation_type,
            "spans": self.spans.get_dict()
        }


class AggregatedSpan:
    def __init__(self, sum_elapsed_time=0):
        self.sum_elapsed_time = sum_elapsed_time

    def get_dict(self):
        return {k: v for k, v in vars(self).items()}


class AggregatedSpans:
    def __init__(self):
        self.Custom = AggregatedSpan()
        self.HTTP = AggregatedSpan()
        self.Middleware = AggregatedSpan()
        self.Redis = AggregatedSpan()
        self.SQL = AggregatedSpan()
        self.View = AggregatedSpan()
        self.Rendering = AggregatedSpan()
        self.Python = AggregatedSpan()

    def get_dict(self):
        return {k: v.get_dict() for k, v in vars(self).items()}

    def get_json(self):
        return json.dumps(self.get_dict())

    def get_mixed_with(self, mix_with):
        mix_with: AggregatedSpans
        mixed_object = AggregatedSpans()
        for span_name in vars(self).keys():
            mixed_object.__setattr__(span_name,
                                     AggregatedSpan(
                                         self.__getattribute__(span_name).sum_elapsed_time + mix_with.__getattribute__(
                                             span_name).sum_elapsed_time))
        return mixed_object


class AggregateData:
    def __init__(self, app, token, start_time=datetime.now().strftime('%Y-%m-%d %H:%M'), sum_elapsed_time=0,
                 num_operations=0, spans=None, operations_summary=None):
        self.app = app
        self.token = token
        self.start_time = start_time
        self.sum_elapsed_time = sum_elapsed_time
        self.num_operations = num_operations
        self.spans = spans if spans is not None else AggregatedSpans()
        # self.operations = operations if operations is not None else []
        self.operations_summary = operations_summary if operations_summary is not None else dict()

    def get_dict(self):
        # logger.error(f"summary: {self.operations_summary}")
        # logger.error(f"spans: {self.spans}")
        return {
            "app": self.app,
            "token": self.token,
            "start_time": self.start_time,
            "sum_elapsed_time": self.sum_elapsed_time,
            "num_operations": self.num_operations,
            "spans": self.spans.get_dict(),
            "operations_summary": {k: v.get_dict() for k, v in self.operations_summary.items()}
        }

    def get_mixed_with(self, other):
        other: AggregateData
        assert self.app == other.app
        assert self.token == other.token
        assert self.start_time == other.start_time

        return AggregateData(
            app=self.app,
            token=self.token,
            start_time=self.start_time,
            sum_elapsed_time=self.sum_elapsed_time + other.sum_elapsed_time,
            num_operations=self.num_operations + other.num_operations,
            spans=self.spans.get_mixed_with(other.spans),
            operations_summary=self.get_joint_operation_summary_with(other)
        )

    def get_joint_operation_summary_with(self, other):
        all_operation_names = set(list(self.operations_summary.keys()) + list(other.operations_summary.keys()))
        result = dict()
        for operation in all_operation_names:
            result.setdefault(operation, AggregateOperationSummary())

        for operation, details in self.operations_summary.items():
            details: AggregateOperationSummary
            joint_operation_summary: AggregateOperationSummary = result[operation]
            joint_operation_summary.num_operations += details.num_operations
            joint_operation_summary.sum_elapsed_time += details.sum_elapsed_time
            joint_operation_summary.spans = details.spans

        for operation, details in other.operations_summary.items():
            details: AggregateOperationSummary
            joint_operation_summary: AggregateOperationSummary = result[operation]
            joint_operation_summary.num_operations += details.num_operations
            joint_operation_summary.sum_elapsed_time += details.sum_elapsed_time
            joint_operation_summary.spans = joint_operation_summary.spans.get_mixed_with(details.spans)

        return result


def get_blank_aggregate_data(client_unique_info, start_time):
    token, name = client_unique_info.split(':')
    return AggregateData(app=name, token=token, start_time=start_time.strftime('%Y-%m-%d %H:%M'))


class ClientInfo:
    def __init__(self, client_address, name, token):
        self.client_address = client_address
        self.name = name
        self.token = token


class ParseResult:
    def __init__(self, result_type=-1, result=None):
        self.result_type = result_type
        self.result = result


class AggregationDelayHandler:
    def __init__(self, current_aggregate, delayed_aggregate):
        current_aggregate: AggregateData
        delayed_aggregate: AggregateData
        self.current_aggregate = current_aggregate
        self.delayed_aggregate = delayed_aggregate
        self.unique_id = secrets.token_urlsafe(5)

    def append(self, info, is_current, client_unique_info):
        info: OperationInfo
        if is_current:
            selected_aggregate = self.current_aggregate
        else:
            selected_aggregate = self.delayed_aggregate

        # selected_aggregate.operations.append(info)
        selected_aggregate.operations_summary.setdefault(info.operation_name, AggregateOperationSummary())
        operation_summary: AggregateOperationSummary = selected_aggregate.operations_summary[info.operation_name]
        # logger.error(f"1: {operation_summary.get_dict()}")
        selected_aggregate.operations_summary[info.operation_name].num_operations += 1
        selected_aggregate.operations_summary[info.operation_name].sum_elapsed_time += info.elapsed_time
        # logger.error(f"2: {operation_summary.get_dict()}")

        selected_aggregate.num_operations += 1
        selected_aggregate.sum_elapsed_time += info.elapsed_time
        for span in vars(info.spans).keys():
            try:
                selected_aggregate.spans.__getattribute__(span).sum_elapsed_time += info.spans.__getattribute__(span).elapsed_time
                selected_aggregate.operations_summary[info.operation_name].spans.__getattribute__(span).sum_elapsed_time += info.spans.__getattribute__(span).elapsed_time
                # logger.error(f"3: {selected_aggregate.get_dict()}")
            except:
                logger.debug('\n'.join(['*** Failed when trying to append to final data, request:',
                                       traceback.format_exc()]))
                return False

    def get_dict(self):
        if self.current_aggregate is None:
            main_dict = self.delayed_aggregate.get_dict()
        elif self.delayed_aggregate is None:
            main_dict = self.current_aggregate.get_dict()
        else:
            main_dict = self.current_aggregate.get_mixed_with(self.delayed_aggregate).get_dict()
        main_dict.update({'unique_id': self.unique_id})
        return main_dict


class CoreAgent:
    _instance = None

    log_level = ''

    timer_started = False
    timer_thread = None
    daemon = True
    scheduler = sched.scheduler(time.time, time.sleep)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_lock = threading.Lock()
    stop_event = threading.Event()

    endpoints_aggregate_data = {}
    tasks_aggregate_data = {}
    failed_submissions = []

    client_list = {}
    max_failed_retry = 5
    max_failed_submissions_length = 100

    @classmethod
    def run(cls, host='localhost', port=6591):
        try:
            cls.sock.bind((host, port))
            # logger.error(f'Bind successful {os.getpid()}')
            cls.sock.listen()
            while True:
                try:
                    conn, addr = cls.sock.accept()
                except:
                    return False
                if not cls.timer_started:
                    cls.timer_started = True
                    cls.timer_thread = threading.Thread(target=cls.one_minute_scheduler, daemon=True)
                    cls.timer_thread.start()
                thread = threading.Thread(target=cls.listen_to_client, args=(cls, conn,), daemon=True)
                thread.start()

        except OSError as e:
            pass
        except Exception:
            logger.error(
                f'run Exception {os.getpid()}\n{traceback.format_exc()}')

        # logger.error(f'Stopped listening')
        cls.sock.close()

    @classmethod
    def _on_stop(cls):
        cls.sock.close()
        cls._instance.stop()
        super(CoreAgent, cls)._on_stop()

    def listen_to_client(self, conn):
        # logger.error('inside listen_to_client')
        client_address = f'{conn.getpeername()[0]}:{conn.getpeername()[1]}'
        while True:
            try:
                raw_size = conn.recv(4)
                if not raw_size:
                    if client_address in self.client_list:
                        self.client_list.pop(client_address)
                    break
                if len(raw_size) != 4:
                    if client_address in self.client_list:
                        self.client_list.pop(client_address)
                    break
                size = struct.unpack(">I", raw_size)[0]
                remaining_size = size
                data = bytearray(0)

                # logger.error(f"{str(size)} to unpack, cur len: {len(data)}")
                while len(data) < size:
                    recv = conn.recv(remaining_size)
                    data += recv
                    remaining_size -= len(recv)
                data = data.decode('utf-8')
                parsed = get_parsed_message(data)
                result_type, result = parsed.result_type, parsed.result
                if result_type in [ReportType.Task.value, ReportType.Endpoint.value]:
                    if client_address in self.client_list:
                        client_unique_info = f'{self.client_list[client_address].token}:{self.client_list[client_address].name}'
                        self.append_to_aggregate_data(result, client_unique_info)
                    else:
                        logger.debug('break')
                        break
                elif result_type == ReportType.OtherCommands.value:
                    send_to_server(result, result_type)
                elif result_type == ReportType.Register.value:
                    client_token, client_name, register_info = result
                    if client_address not in self.client_list:
                        self.client_list[client_address] = ClientInfo(client_address=client_address, token=client_token,
                                                                      name=client_name)
                    send_to_server(register_info, result_type)
            except OSError as exc:
                logger.error(
                    "CoreAgentSocketThread error on read response: %r", exc, exc_info=exc
                )
                # logger.error(f'listen_to_client\n\n{traceback.format_exc()}')
                # print(f'listen_to_client\n\n{traceback.format_exc()}')
            except Exception:
                logger.error(f'In listen_to_client\n{traceback.format_exc()}')
                # print(f'In listen_to_client\n{traceback.format_exc()}')
        conn.close()

    @staticmethod
    def get_next_minute():
        next_minute = datetime.now() + timedelta(seconds=60)
        next_minute = next_minute.replace(second=1, microsecond=0)
        return datetime.timestamp(next_minute)

    @classmethod
    def one_minute_scheduler(cls):
        while True:
            cls.scheduler.enterabs(cls.get_next_minute(), 1, cls.post_and_refresh)
            cls.scheduler.run()

    @classmethod
    def post_and_refresh(cls):
        try:
            for i, failed_submission in enumerate(cls.failed_submissions[:cls.max_failed_retry]):
                result = send_to_server(failed_submission,
                                        content_type=ReportType.Endpoint.value)
                if result:
                    cls.failed_submissions.pop(i)
                else:
                    log_error(f"FAIL RETRY {datetime.now()}")
        except:
            log_error(f"{datetime.now()}\n{traceback.format_exc()}")

        cls.data_lock.acquire()
        for key in cls.endpoints_aggregate_data.keys():
            try:
                windows = list(cls.endpoints_aggregate_data[key].keys())
                windows.sort()
                for i, window in enumerate(windows):
                    data_to_send = {'BatchReportEndpoints': cls.endpoints_aggregate_data[key][window].get_dict()}
                    # logger.error(data_to_send)
                    result = send_to_server(data_to_send,
                                            content_type=ReportType.Endpoint.value)
                    if not result:
                        if len(cls.failed_submissions) < cls.max_failed_submissions_length:
                            cls.failed_submissions.append(data_to_send)
                        log_error(f"Fail {datetime.now()} {window} {cls.endpoints_aggregate_data[key][window].get_dict()['num_operations']}")
                    cls.endpoints_aggregate_data[key].pop(window)
            except:
                logger.error(traceback.format_exc())
            finally:
                now_window = datetime.now().replace(second=0, microsecond=0)
                if now_window not in cls.endpoints_aggregate_data[key]:
                    cls.endpoints_aggregate_data[key][now_window] = AggregationDelayHandler(
                        current_aggregate=get_blank_aggregate_data(client_unique_info=key, start_time=datetime.now()),
                        delayed_aggregate=get_blank_aggregate_data(client_unique_info=key, start_time=datetime.now()))

        for key in cls.tasks_aggregate_data.keys():
            try:
                windows = list(cls.tasks_aggregate_data[key].keys())
                windows.sort()
                for i, window in enumerate(windows):
                    data_to_send = {'BatchReportTasks': cls.tasks_aggregate_data[key][window].get_dict()}
                    result = send_to_server(data_to_send,
                                            content_type=ReportType.Task.value)
                    if not result:
                        if len(cls.failed_submissions) < cls.max_failed_submissions_length:
                            cls.failed_submissions.append(data_to_send)
                        log_error(f"Fail {datetime.now()} {window} {cls.tasks_aggregate_data[key][window].get_dict()['num_operations']}")
                    cls.tasks_aggregate_data[key].pop(window)

            except:
                logger.error(traceback.format_exc())
            finally:
                now_window = datetime.now().replace(second=0, microsecond=0)
                if now_window not in cls.tasks_aggregate_data[key]:
                    cls.tasks_aggregate_data[key][now_window] = AggregationDelayHandler(
                        current_aggregate=get_blank_aggregate_data(client_unique_info=key, start_time=datetime.now()),
                        delayed_aggregate=get_blank_aggregate_data(client_unique_info=key, start_time=datetime.now()))
        cls.data_lock.release()

    @classmethod
    def append_to_aggregate_data(cls, info, client_unique_info):
        info: OperationInfo
        start_window_time = info.start_time.replace(second=0, microsecond=0)
        now_time = datetime.now()
        is_current = now_time.minute == start_window_time.minute
        data_type = info.operation_type
        try:
            cls.data_lock.acquire()
            if data_type == ReportType.Endpoint.value:
                target_aggregate_data = cls.endpoints_aggregate_data
            elif data_type == ReportType.Task.value:
                target_aggregate_data = cls.tasks_aggregate_data
            else:
                return False

            if client_unique_info not in target_aggregate_data:
                target_aggregate_data[client_unique_info] = dict()
            client_aggregate_data = target_aggregate_data[client_unique_info]

            if start_window_time not in client_aggregate_data:
                delayed_aggregate = get_blank_aggregate_data(client_unique_info, start_window_time)
                current_aggregate = get_blank_aggregate_data(client_unique_info, start_window_time)

                client_aggregate_data[start_window_time] = AggregationDelayHandler(
                    current_aggregate=current_aggregate,
                    delayed_aggregate=delayed_aggregate)

            delay_handler: AggregationDelayHandler = client_aggregate_data[start_window_time]
            delay_handler.append(info, is_current, client_unique_info)

            cls.data_lock.release()
            return True
        except:
            cls.data_lock.release()
            logger.error(traceback.format_exc())
            return False


def tree_traverse(span_tree_root):
    spans = Spans()
    queue = [span_tree_root]
    while queue:
        current = queue.pop()
        total_time = current.elapsed_time
        for child in current.children:
            queue.append(child)
            total_time -= child.elapsed_time
        spans.__getattribute__(get_span_name(current.span_name)).elapsed_time += total_time
    for span_name in vars(spans).keys():
        spans.__getattribute__(span_name).elapsed_time = round(spans.__getattribute__(span_name).elapsed_time / 1000, 1)
    return spans


def get_parsed_operation(request_dict):
    try:
        parent_child_dict = {}
        id_to_span_object = {}

        result_type = ReportType.Endpoint.value
        commands = request_dict['BatchCommand']['commands']
        try:
            request_start_time = datetime.strptime(commands.pop(0)['StartRequest']['timestamp'],
                                                   '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            request_start_time = datetime.strptime(commands.pop(0)['StartRequest']['timestamp'],
                                                   '%Y-%m-%dT%H:%M:%SZ')
        try:
            request_finish_time = datetime.strptime(commands.pop(-1)['FinishRequest']['timestamp'],
                                                    '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            request_finish_time = datetime.strptime(commands.pop(-1)['FinishRequest']['timestamp'],
                                                    '%Y-%m-%dT%H:%M:%SZ')
        request_elapsed_time = request_finish_time - request_start_time
        request_elapsed_time_us = timedelta_to_us(request_elapsed_time)
        request_method = None
        while True:
            command = commands[0]
            if 'TagRequest' in command:
                command = command['TagRequest']
                if command['tag'] == 'task_id':
                    result_type = ReportType.Task.value
                elif command['tag'] == 'method':
                    request_method = command['value'].upper()
                commands.pop(0)
            else:
                break

        commands.reverse()
        for command in commands:
            if 'TagSpan' in command:
                continue
            elif 'StopSpan' in command:
                command = command['StopSpan']
                span_id = command['span_id']
                try:
                    stop_time = datetime.strptime(command['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
                except:
                    stop_time = datetime.strptime(command['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
                continue

            elif 'StartSpan' in command:
                command = command['StartSpan']

                parent_id = command['parent_id']
                name = command['operation']
                if get_span_name(name) == 'View' or get_span_name(name) == 'Python':
                    operation_name = name.split('/')[1]

                try:
                    start_time = datetime.strptime(command['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
                except:
                    start_time = datetime.strptime(command['timestamp'], '%Y-%m-%dT%H:%M:%SZ')

                elapsed_time = timedelta_to_us(stop_time - start_time)

                if parent_id is None:
                    span_tree_root = Span(span_id, name, elapsed_time)
                try:
                    parent_child_dict[parent_id].append(span_id)
                except KeyError:
                    parent_child_dict[parent_id] = [span_id]
                id_to_span_object[span_id] = Span(span_id, name, elapsed_time)

        for parent, children in parent_child_dict.items():
            for child in children:
                try:
                    id_to_span_object[parent].children.append(id_to_span_object[child])
                except:
                    span_tree_root.children.append(id_to_span_object[child])

        spans = tree_traverse(span_tree_root)

        if request_method is not None:
            operation_name = f'{operation_name}@{request_method}'
        return ParseResult(result_type=result_type,
                           result=OperationInfo(elapsed_time=round(request_elapsed_time_us / 1000, 1),
                                                operation_type=result_type,
                                                start_time=request_start_time,
                                                operation_name=operation_name,
                                                spans=spans))
    except:
        logger.error(traceback.format_exc())


def get_parsed_registration(command_dict):
    try:
        return ParseResult(result_type=ReportType.Register.value,
                           result=[command_dict['Register']['key'],
                                   command_dict['Register']['app'],
                                   command_dict])
    except:
        return None


def get_parsed_message(message):
    message_dict = json.loads(message)
    if 'BatchCommand' in message_dict:
        return get_parsed_operation(message_dict)
    elif 'Register' in message_dict:
        return get_parsed_registration(message_dict)
    elif type(message_dict) == dict:
        return ParseResult(result_type=ReportType.OtherCommands.value, result=message_dict)


if __name__ == '__main__':
    tcp_host = 'localhost'
    tcp_port = 6591

    signal.signal(signal.SIGTERM, farewell)
    CoreAgent.run(host=tcp_host, port=tcp_port)
