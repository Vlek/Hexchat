import hexchat

__module_name__ = 'Eval'
__module_version__ = '0.0.1'
__module_description__ = "Evals and prints what's thrown to the '?' command"
__module_author__ = 'Vlek'

throwchair = "(╯°□°）╯︵ ┻━┻"
cry = "(╥﹏╥)"
lenny = "( ͡° ͜ʖ ͡°)"
shrug = "¯_(ツ)_/¯"
rifle = "︻デ═一"

def evaluate(word, word_to_eol, userdata):
    hexchat.command('say {}'.format(str(eval(word_to_eol[1]))))
    return hexchat.EAT_ALL

hexchat.hook_command("?", evaluate, help="/? (Command to evaluate and print out)")
