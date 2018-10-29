import logging
from datetime import timedelta
from time import sleep

import yaml
from vk_api import VkApi

_logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # read config
    with open('config.yml') as f:
        config = yaml.load(f)

    # check config
    if 'vk_token' in config:
        if not isinstance(config['vk_token'], str):
            raise ValueError(f'invalid vk_token in config, '
                             f'must be string, got {type(config["vk_token"])}')
    else:
        raise ValueError('required vk_token in config')

    if 'autoread_all_muted' in config and config['autoread_all_muted'] is not None:
        if not isinstance(config['autoread_all_muted'], bool):
            raise ValueError(f'invalid autoread_all_muted in config, '
                             f'must be bool, got {type(config["autoread_all_muted"])}')
    else:
        config['autoread_all_muted'] = False

    if 'always_autoread_chats' in config and config['always_autoread_chats'] is not None:
        if not isinstance(config['always_autoread_chats'], list):
            raise ValueError(f'invalid always_autoread_chats in config, '
                             f'must be list of strings, got {type(config["always_autoread_chats"])}')
        if len(config['always_autoread_chats']) != 0:
            if not all(isinstance(it, str) for it in config['always_autoread_chats']):
                raise ValueError('invalid always_autoread_chats in config, '
                                 'must be list of strings')
    else:
        config['always_autoread_chats'] = list()

    if 'deny_autoread_chats' in config and config['deny_autoread_chats'] is not None:
        if not isinstance(config['deny_autoread_chats'], list):
            raise ValueError(f'invalid deny_autoread_chats in config, '
                             f'must be list of strings, got {type(config["deny_autoread_chats"])}')
        if len(config['deny_autoread_chats']) != 0:
            if not all(isinstance(it, str) for it in config['deny_autoread_chats']):
                raise ValueError('invalid deny_autoread_chats in config, '
                                 'must be list of strings')
    else:
        config['deny_autoread_chats'] = list()

    # setup vk
    vk_session = VkApi(token=config['vk_token'])
    vk = vk_session.get_api()

    # start daemon
    while True:
        dialogs = vk.messages.getConversations(filter='unread', count=5)
        dialogs = dialogs['items']

        for it in dialogs:
            it = it['conversation']

            if 'chat_settings' not in it:
                continue

            if 'title' not in it['chat_settings']:
                continue

            peed_id = it['peer']['id']
            title = it['chat_settings']['title']
            is_muted = 'disabled_until' in it.get('push_settings', dict())

            do_autoread = False
            if config['autoread_all_muted'] and is_muted:
                do_autoread = True
            if any(title.lower() in config_title.lower() for config_title in config['always_autoread_chats']):
                do_autoread = True
            if any(title.lower() in config_title.lower() for config_title in config['deny_autoread_chats']):
                do_autoread = False

            if do_autoread:
                _logger.info(f'Marking as read chat with title {title}')
                vk.messages.markAsRead(peer_id=peed_id)

        sleep(timedelta(seconds=5).total_seconds())
