import hexchat

__module_name__ = 'Hilight Responses'
__module_version__ = '0.0.1'
__module_description__ = 'Highlights messages after yours'
__module_author__ = 'Vlek'

_lastresponder = {}

def check_for_highlight(word, word_to_eol, userdata):
    global _lastresponder
    channelname = hexchat.get_context().get_info('channel')
    windowname = hexchat.find_context().get_info('channel')
    if channelname in _lastresponder and _lastresponder[channelname] == hexchat.get_info('nick') and windowname != channelname:
        if len(word) == 2:
            word.append('')
        hexchat.emit_print('Channel Msg Hilight', word[0], word[1], word[2])
        return hexchat.EAT_ALL
    update_responder(word, word_to_eol, userdata)
    return hexchat.EAT_NONE

def update_responder(word, word_to_eol, userdata):
    global _lastresponder
    _lastresponder[hexchat.get_context().get_info('channel')] = word[0]
    return hexchat.EAT_NONE

hexchat.hook_print('Channel Message', check_for_highlight, priority=hexchat.PRI_LOW)
hexchat.hook_print('Your Message', update_responder, priority=hexchat.PRI_LOW)
hexchat.hook_print('Channel Msg Hilight', update_responder, priority=hexchat.PRI_LOW)
