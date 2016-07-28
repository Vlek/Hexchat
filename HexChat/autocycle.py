import hexchat

__module_name__ = 'Autocycle'
__module_version__ = '0.0.1'
__module_description__ = 'Cycles channel to get OPd if last in'
__module_author__ = 'Vlek'


def cycle_check(argv, arg_to_eol, c):
    context = hexchat.find_context()
    if len(context.get_list('users')) == 1:
        context.command('/cycle')


for event in ['Part', 'Part with Reason', 'Quit']:
    hexchat.hook_print(event, cycle_check, priority=hexchat.PRI_LOW)
