import hexchat

#Based on Weechat's Weestats: https://weechat.org/scripts/source/weestats.py.html/
#By Filip H.F. 'FiXato' Slagter <fixato [at] gmail [dot] com>

__module_name__ = 'HexStats'
__module_version__ = '0.0.1'
__module_description__ = 'Displays HexChat Wide User Statistics'
__module_author__ = 'Vlek'


def stats(word, word_to_eol, userdata):
    context = hexchat.find_context()
    chans = hexchat.get_list('channels')
    types = [i.type for i in chans]
    channels = types.count(2)
    ops = 0
    servers = types.count(1)
    queries = types.count(3)
    context.prnt('Stats: {} channels ({} OPs), {} servers, {} queries'.format( channels, ops,
                                                                               servers, queries ))
    return hexchat.EAT_ALL

hexchat.hook_command("stats", stats, help="/stats displays HexChat user statistics")
