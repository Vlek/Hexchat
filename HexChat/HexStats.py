import hexchat

#Based on Weechat's Weestats: https://weechat.org/scripts/source/weestats.py.html/
#By Filip H.F. 'FiXato' Slagter <fixato [at] gmail [dot] com>

__module_name__ = 'HexStats'
__module_version__ = '0.0.1'
__module_description__ = 'Displays HexChat Wide User Statistics'
__module_author__ = 'Vlek'


def stats(word, word_to_eol, userdata):
    print( getstats() )
    return hexchat.EAT_ALL


def printstats(word, word_to_eol, userdata):
    context = hexchat.find_context()
    context.command('say {}'.format( getstats() ))
    return hexchat.EAT_ALL


def getstats():
    chans = hexchat.get_list('channels')
    types = [i.type for i in chans]
    channels = types.count(2)
    
    contextlist = [i.context for i in chans if i.type == 2]
    ops = []
    for context in contextlist:
        ops += [user.prefix for user in context.get_list('users') if user.nick == hexchat.get_info('nick')]
    #ops = ops.count('@')

    servers = types.count(1)
    queries = types.count(3)
    return 'Stats: {} channels ({} OPs), {} servers, {} queries'.format( channels, ops,
                                                                        servers, queries )


hexchat.hook_command("stats", stats, help="/stats displays HexChat user statistics")
hexchat.hook_command("printstats", printstats, help="/printstats Says HexChat user statistics in current context")


