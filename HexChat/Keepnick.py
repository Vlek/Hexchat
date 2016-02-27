import hexchat

__module_name__ = 'Keepnick'
__module_version__ = '0.0.1'
__module_description__ = "Attempts to get one's preferred nickname"
__module_author__ = 'Vlek'

def attempt_nick_change():
    context = hexchat.find_context()
    if hexchat.get_info('nick') != hexchat.get_prefs("irc_nick1"):
        context.command('nick {}'.format(hexchat.get_prefs("irc_nick1")))
        return True
    return False


# If we log on and our nick is not our preferred nick,
if hexchat.get_info('nick') != hexchat.get_prefs("irc_nick1"):

    # If there's nickserv, we're going to have a password on file for it,
    # And, if that's the case, we'll just do the usual stuff to get our nick
    if hexchat.get_info('nickserv') != None:
        preferednick = hexchat.get_prefs("irc_nick1")
        hexchat.command('msg nickserv ghost {} {}; nick {}'.format( preferednick,
                                                                    hexchat.get_info('nickserv'),
                                                                    preferednick) )

    # Otherwise we have to get creative and dirty. Every twelve seconds we'll
    # Ask the server whether we can have our preferred nick until we get it.
    else:
        hexchat.hook_timer(12000, attempt_nick_change)
