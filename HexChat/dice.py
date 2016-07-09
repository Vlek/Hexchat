import parsley, hexchat
from random import randint

__module_name__ = 'dice'
__module_version__ = '1.0.0'
__module_description__ = 'Allows one to do emote dice rolls'
__module_author__ = 'Vlek'

def say(msg):
    """Says msg in chat within current context"""
    context = hexchat.find_context()
    context.command('say {}'.format(msg))
    return

def calculate(start, pairs):
    result = start
    for op, value in pairs:
        if op == '+':
            result += value
        elif op == '-':
            result -= value
        elif op == '*':
            result *= value
        elif op == '/':
            result /= value
    return result

def roll(num_dice, dice_sides):
    num_dice = int(num_dice) if num_dice != '' else 1
    return sum([randint(1, int(dice_sides)) for i in range(num_dice)])

x = parsley.makeGrammar("""
number = <digit+>:ds -> int(ds)
parens = '(' ws expr:e ws ')' -> e
die = <digit*>:dice_num 'd' <digit+>:dice_sides -> roll(dice_num, dice_sides)
value = die | number | parens
ws = ' '*
add = '+' ws expr2:n -> ('+', n)
sub = '-' ws expr2:n -> ('-', n)
mul = '*' ws value:n -> ('*', n)
div = '/' ws value:n -> ('/', n)
addsub = ws (add | sub)
muldiv = ws (mul | div)
expr = expr2:left addsub*:right -> calculate(left, right)
expr2 = value:left muldiv*:right -> calculate(left, right)
""", {"calculate": calculate, "roll": roll})


def dice(word, word_to_eol, userdata):
    if len(word) == 1:
        say('//help dice')
    roll_expr = ''.join(word[1:])
    context = hexchat.find_context()
    context.command('me {}'.format("rolls {}: {}".format(roll_expr, x(roll_expr).expr())))
    return hexchat.EAT_ALL

for command in ['dice', 'roll']:
    hexchat.hook_command(command, dice, help="/roll 1d20 + 3")

