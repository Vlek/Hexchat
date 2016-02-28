import hexchat
 
#Based on Weechat's Weestats: https://weechat.org/scripts/source/weestats.py.html/
#By Filip H.F. 'FiXato' Slagter <fixato [at] gmail [dot] com>
 
__module_name__ = 'HexStats'
__module_version__ = '0.0.1'
__module_description__ = 'Displays HexChat-wide User Statistics'
__module_author__ = 'Vlek'
 
 
def stats(word, word_to_eol, userdata):
    print( getstats() )
    return hexchat.EAT_ALL
 
def printstats(word, word_to_eol, userdata):
    hexchat.command('say {}'.format( getstats() ))
    return hexchat.EAT_ALL
 
def check_opped(ctx, nickprefixes):
    op_idx = nickprefixes.index('@')
    nick = ctx.get_info('nick')
    me = [user for user in ctx.get_list('users') if hexchat.nickcmp(user.nick, nick) == 0][0]
    if me.prefix and nickprefixes.index(me.prefix[0]) <= op_idx:
        return True
    return False
 
def getstats():
    contexts = hexchat.get_list('channels')
 
    channels = 0
    servers = 0
    queries = 0
    ops = 0
    for ctx in contexts:
        if ctx.type == 1:
            servers += 1
        elif ctx.type == 2:
            channels += 1
            if check_opped(ctx.context, ctx.nickprefixes):
                ops += 1
        elif ctx.type == 3:
            queries += 1
 
    return 'Stats: {} channels ({} OPs), {} servers, {} queries'.format( channels, ops,
                                                                        servers, queries )
 
 
hexchat.hook_command("stats", stats, help="/stats displays HexChat user statistics")
hexchat.hook_command("printstats", printstats, help="/printstats Says HexChat user statistics in current context")
