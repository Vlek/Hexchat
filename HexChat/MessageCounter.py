import hexchat

__module_name__ = 'Message Count'
__module_version__ = '0.0.1'
__module_description__ = 'Message Count in Channel Name'
__module_author__ = 'Vlek'

_channelmessages = {}


def update_count(argv, arg_to_eol, c):
    currentcontext = hexchat.find_context()
    currentcontextchannel = currentcontext.get_info('channel').split()[0]
    
    channelcontext = hexchat.get_context()
    channelname = channelcontext.get_info('channel').split()[0]

    # Add to the message count
    if currentcontextchannel != channelname:
        if channelname not in _channelmessages:
            _channelmessages[channelname] = 0
        
        _channelmessages[channelname] += 1
        channelcontext.command("settab {} ({})".format( channelname, _channelmessages[channelname] ))
        
    # If we're either shifting to the tab or there's a new message in our active tab,
    else:
        channelcontext.command("settab {}".format( channelname ))
        _channelmessages[channelname] = 0


hexchat.hook_print('Channel Message', update_count, priority=hexchat.PRI_LOW)
hexchat.hook_print('Channel Msg Hilight', update_count, priority=hexchat.PRI_LOW)
hexchat.hook_print('Channel Action', update_count, priority=hexchat.PRI_LOW)
hexchat.hook_print('Channel Action Hilight', update_count, priority=hexchat.PRI_LOW)
hexchat.hook_print('Focus Tab', update_count)
