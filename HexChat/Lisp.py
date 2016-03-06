import hexchat, re

__module_name__ = 'Lisp'
__module_version__ = '0.0.1'
__module_description__ = "Creates a lisp command to lisp one's speech"
__module_author__ = 'Vlek'


def say(msg):
    """Says msg in chat within current context"""
    context = hexchat.find_context()
    context.command('say {}'.format(msg))
    return


def lisp(word, word_to_eol, userdata):
    msg = re.sub("s(?!h)", "sh", ' '.join(word[1:]), flags=re.IGNORECASE)
    say( msg )
    return hexchat.EAT_ALL


hexchat.hook_command('lisp',lisp,help="/lisp (Sentence to auto-lisp s's to sh's)") 
