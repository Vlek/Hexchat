import hexchat

__module_name__ = 'greyignore'
__module_version__ = '0.0.1'
__module_description__ = 'Makes ignored people hard to read'
__module_author__ = 'Vlek'

_ignorelist = hexchat.get_pluginpref('greyignore')

if _ignorelist == None:
    _ignorelist = []
else:
    _ignorelist = _ignorelist.split(',')

def check_ignore(word, word_to_eol, userdata):
    ignoretarget = word[0]
    for user in _ignorelist:
            if hexchat.nickcmp(user, ignoretarget) == 0:
                context = hexchat.get_context()
                if len(word) == 2:
                    word.append('')
                context.prnt('\x0314{}{} {}'.format(word[2], ignoretarget, word[1]))
                return hexchat.EAT_ALL

def ignore(word, word_to_eol, userdata):
    ignoretarget = word[1]
    for user in _ignorelist:
        if hexchat.nickcmp(user, ignoretarget) == 0:
            print('User {} already in ignore list'.format(ignoretarget))
            return hexchat.EAT_ALL
    print('Ignoring {}'.format(ignoretarget))
    _ignorelist.append(ignoretarget)
    hexchat.set_pluginpref('greyignore', ','.join(_ignorelist))
    return hexchat.EAT_ALL

def unignore(word, word_to_eol, userdata):
    unignoretarget = word[1]
    try:
        _ignorelist.remove(unignoretarget)
        print('Unignoring {}'.format(unignoretarget))
        hexchat.set_pluginpref('greyignore', ','.join(_ignorelist))
    except ValueError:
        print('{} not found in ignore list'.format(unignoretarget))
    return hexchat.EAT_ALL

hexchat.hook_command('ignore', ignore)
hexchat.hook_command('unignore', unignore)
hexchat.hook_print('Channel Msg Hilight', check_ignore, priority=hexchat.PRI_LOW)
hexchat.hook_print('Channel Message', check_ignore, priority=hexchat.PRI_LOW)


