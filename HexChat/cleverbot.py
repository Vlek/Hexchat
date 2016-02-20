import hexchat, cleverbot, time

__module_name__ = 'Cleverbot'
__module_version__ = '0.0.1'
__module_description__ = 'Cleverbot Response Bot'
__module_author__ = 'Vlek'


_seconds_between_responses = 5
_cb = cleverbot.Cleverbot()
_lastresponse = time.time()


def speechhandler( argv, argv_to_eol, c ):
    global _lastresponse, _seconds_between_responses
    if time.time() - _lastresponse >= _seconds_between_responses:
        context = hexchat.get_context()
        
        response = _cb.ask( argv[1:] )
        time.sleep(3)
        context.command('say {}'.format( response ) )

        _lastresponse = time.time()
        
    return hexchat.EAT_NONE


hexchat.hook_print('Channel Message', speechhandler, priority=hexchat.PRI_LOW)
hexchat.hook_print('Channel Msg Hilight', speechhandler, priority=hexchat.PRI_LOW)
