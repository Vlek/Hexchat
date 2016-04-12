import hexchat

__module_name__ = 'Eval'
__module_version__ = '0.0.1'
__module_description__ = "Evals and prints what's thrown to the '?' command"
__module_author__ = 'Vlek'

colors = {'white':0, 'black':1, 'blue':2, 'green':3, 'red':4,
           'brown':5, 'purple':6, 'orange':7, 'yellow':8, 'green':9,
           'cyan':10, 'lightcyan':11, 'lightblue':12, 'pink':13,
           'grey':14, 'lightgrey':15}

#Red, yellow, teal, light blue, pink
_colorful = [4, 8, 9, 12, 13]

throwchair = "(╯°□°）╯︵ ┻━┻"
cry = "(╥﹏╥)"
lenny = "( ͡° ͜ʖ ͡°)"
shrug = "¯_(ツ)_/¯"
rifle = "︻デ═一"

def color(s, color='red'):
    return '\x03{}{}\00399'.format(colors[color], s)

def colorful(s):
    output = []
    result = []
    index = 0
    l = len(_colorful) - 1
    for w in s:
        for char in w:
            if index > l:
                index = 0
            output.append( '\x03{}{}'.format(_colorful[index],char) )
            index += 1
        result.append(''.join(output))
        output = []
    return ''.join(result)

def reverse(s):    
    return s[::-1]

def evaluate(word, word_to_eol, userdata):
    hexchat.command('say {}'.format(str(eval(word_to_eol[1]))))
    return hexchat.EAT_ALL

hexchat.hook_command("?", evaluate, help="/? (Command to evaluate and print out)")
