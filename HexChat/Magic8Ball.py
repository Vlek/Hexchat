import hexchat
from random import choice

__module_name__ = 'Magic8ball'
__module_version__ = '0.0.1'
__module_description__ = 'Allows one ask magic8ball questions with answers'
__module_author__ = 'Vlek'

_8ball_answers = [
    'It is certain', 'It is decidedly so',
    'Without a doubt', 'Yes, definitely',
    'You may rely on it', 'As I see it, yes',
    'Most likely', 'Outlook good',
    'Yes', 'Signs point to yes',
    'Reply hazy, try again', 'Ask again later',
    'Better not tell you now', 'Cannot predict now',
    'Concentrate and ask again', "Don't count on it",
    'My reply is no', 'My sources say no',
    'Outlook not so good', 'Very doubtful']

def ask8ball(word, word_to_eol, userdata):
    if len(word) == 1:
        say('/help 8ball')
    context = hexchat.find_context()
    #Magic8Ball... will this malware be more effective if it has a fancy GUI? ... 'Outlook good'
    context.prnt("Magic8Ball... {}? .. '{}'".format(' '.join(word[1:]), choice(_8ball_answers)))
    return hexchat.EAT_ALL

for command in ['magic8ball', '8ball']:
    hexchat.hook_command(command, ask8ball, help="/8ball (question)")

