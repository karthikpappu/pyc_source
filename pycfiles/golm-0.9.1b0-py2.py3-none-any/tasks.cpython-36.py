# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/tasks.py
# Compiled at: 2018-04-15 14:10:04
# Size of source mod 2**32: 4678 bytes
import logging, time, traceback
from celery import shared_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings
from core import message_logger
from core.chat_session import ChatSession
from core.interfaces.all import create_from_name
from core.persistence import get_redis
logger = get_task_logger(__name__)

@shared_task
def accept_user_message(session: dict, raw_message):
    from core.dialog_manager import DialogManager
    session = ChatSession.from_json(session)
    print('Accepting message - chat id {}, message: {}'.format(session.chat_id, raw_message))
    dialog = DialogManager(session)
    parsed = session.interface.parse_message(raw_message)
    _process_message(dialog, parsed)
    should_log_messages = settings.GOLEM_CONFIG.get('SHOULD_LOG_MESSAGES', False)
    if should_log_messages:
        if 'text' in raw_message:
            text = raw_message['text']
            message_logger.on_message.delay(session, text, dialog, from_user=True)


def setup_schedule_callbacks(sender, callback):
    callbacks = settings.GOLEM_CONFIG.get('SCHEDULE_CALLBACKS')
    if not callbacks:
        return
    for name in callbacks:
        params = callbacks[name]
        print('Scheduling task {}: {}'.format(name, params))
        if isinstance(params, dict):
            cron = crontab(**params)
        else:
            if isinstance(params, int):
                cron = params
            else:
                raise Exception('Specify either number of seconds or dict of celery crontab params (hour, minute): {}'.format(params))
        sender.add_periodic_task(cron, callback.s(name))
        print(' Scheduled for {}'.format(cron))


def accept_schedule_all_users(callback_name):
    print('Accepting scheduled callback {}'.format(callback_name))
    db = get_redis()
    interface_names = db.hgetall('session_interface')
    for uid in interface_names:
        interface_name = interface_names[uid].decode('utf-8')
        interface = create_from_name(interface_name)
        session = ChatSession(interface, uid.decode('utf-8'))
        accept_schedule_callback(session.to_json(), callback_name)


@shared_task
def accept_schedule_callback(session: dict, callback_name):
    session = ChatSession.from_json(session)
    from core.dialog_manager import DialogManager
    db = get_redis()
    active_time = float(db.hget('session_active', session.chat_id).decode('utf-8'))
    inactive_seconds = time.time() - active_time
    print('{} from {} was active {}'.format(session.chat_id, session.interface, active_time))
    parsed = {'type':'schedule', 
     'entities':{'intent':'_schedule', 
      '_inactive_seconds':inactive_seconds, 
      '_callback_name':callback_name}}
    dialog = DialogManager(session)
    _process_message(dialog, parsed)


@shared_task
def accept_inactivity_callback(session: dict, context_counter, callback_name, inactive_seconds):
    session = ChatSession.from_json(session)
    from core.dialog_manager import DialogManager
    dialog = DialogManager(session)
    if dialog.context.counter != context_counter:
        print('Canceling inactivity callback after user message.')
        return
    parsed = {'type':'schedule', 
     'entities':{'intent':'_inactive', 
      '_inactive_seconds':inactive_seconds, 
      '_callback_name':callback_name}}
    _process_message(dialog, parsed)


def _process_message(dialog, parsed):
    try:
        dialog.process(parsed['type'], parsed['entities'])
    except Exception as e:
        print('!!!!!!!!!!!!!!!! EXCEPTION AT MESSAGE QUEUE !!!!!!!!!!!!!!!', e)
        traceback.print_exc()
        dialog.logger.log_error(exception=e, state=(dialog.current_state_name))


@shared_task
def fake_move_to_state(chat_id, state: str, entities=()):
    session = get_redis().hget('chat_session', chat_id)
    if not (session and state):
        logging.warning('ChatSession or State is null')
        return
    import json
    session = json.loads(session.decode('utf-8'))
    session = ChatSession.from_json(session)
    state = str(state)
    from core.dialog_manager import DialogManager
    logger.debug('Moving chat id {} to state {}'.format(session.chat_id, state))
    dialog = DialogManager(session)
    msg_data = {'_state': state}
    for k, v in entities:
        msg_data[k] = [
         {'value': v}]

    dialog.process('postback', msg_data)