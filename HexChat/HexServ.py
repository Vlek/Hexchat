import hexchat, os

__module_name__ = 'HexServ'
__module_version__ = '0.1.0'
__module_description__ = 'File server for Hexchat'
__module_author__ = 'Vlek'
__module_website__ = 'https://github.com/Vlek/HexServ'

_servingchannel = "#uosteam"
_serving = True

_scriptsDirectory = "C:/scripts/"
_files= [f for f in os.listdir(_scriptsDirectory) if os.path.isfile(os.path.join(_scriptsDirectory, f))]

def announce():
	print("{} v{} by {}: {}".format(__module_name__, __module_version__, __module_author__, __module_website__))

def help():
	print "HexServ Commands:"
	print "   \002/hexserv help\002:    Commands list"
	print "   \002/hexserv start\002:   Starts HexServ File Transfers"
	print "   \002/hexserv stop\002:    Stops HexServ File Transfers"
	print "   \002/hexserv channel\002: Changes HexServ's Serving Channel"
	print "   \002/hexserv dir\002:     Changes HexServ's Serving File Directory"
	print "   \002/hexserv ban\002:     Bans a user from using HexServ"

def hexserv_stop(x):
    """Halts hexserv from allowing searches or sending files"""
    global _serving
    _serving = False
    print('HexServ - File transferring deactivated!')
    return hexchat.EAT_ALL

def hexserv_start(x):
    """Makes hexserv allow searches and sending files"""
    global _serving
    _serving = True
    print('HexServ - File transferring activated!')
    return hexchat.EAT_ALL

def hexserv_channel(chan):
    return hexchat.EAT_ALL

def hexserv_ban(user):
    return hexchat.EAT_ALL

def hexserv_dispatch(argv, arg_to_eol, c):
    if len(argv) == 1:
        announce()
        return hexchat.EAT_ALL
    try:
        {
        "help" : help,
        "stop" : hexserv_stop,
        "start": hexserv_start,
        "ban"  : hexserv_ban
        }[argv[1]](argv[1:])
    except:
	help()
    return hexchat.EAT_ALL

def hexserv_search(user, searchterm):
    print('Searching for {}...'.format(searchterm))
    return hexchat.EAT_NONE

def hexserv_find(user, searchterm):
    print('Performing find for {}...'.format(searchterm))
    return hexchat.EAT_NONE

def hexserv_request(user, searchterm):
    print('Saving request for {}'.format(searchterm))
    return hexchat.EAT_NONE

def hexserv_get(user, filename):
    #print('Sending file {}'.format(filename))
    if len(filename) == 1 and filename[0].lower() in ['help', '']:
        hexchat.command('msg {} Commands: !search, !find, !request, !get, !vlek'.format(user))
    if ' '.join(filename) in _files:
        hexchat.command('dcc send {} "{}"'.format(user, _scriptsDirectory + ' '.join(filename)))
    else:
        hexchat.command('msg {} File Not Found: {}'.format(user, ' '.join(filename)))
    return hexchat.EAT_NONE

def hexserv_usercommands_dispatch(argv, arg_to_eol, c):
    global _serving
    if hexchat.get_info('channel') != _servingchannel or len(argv) == 1 or not _serving:
        return hexchat.EAT_NONE
    try:
        a = argv[1].split()
        {
        "@search"  : hexserv_search,
        "!search"  : hexserv_search,
        "@find"    : hexserv_find,
        "!find"    : hexserv_find,
        "@request" : hexserv_request,
        "!request" : hexserv_request,
        "!" + hexchat.get_info('nick').lower() : hexserv_get
        }[a[0].lower()](argv[0],a[1:])
    except:
        pass
    return hexchat.EAT_NONE

def removemenu(dt):
    hexchat.command('MENU DEL HexServ')

hexchat.hook_command("hexserv", hexserv_dispatch, help="/hexserv help for commands.")
hexchat.hook_print('Channel Msg Hilight', hexserv_usercommands_dispatch)
hexchat.hook_print('Channel Message', hexserv_usercommands_dispatch)
hexchat.hook_print('Private Message to Dialog', hexserv_usercommands_dispatch)
hexchat.hook_print("Private Action to Dialog", hexserv_usercommands_dispatch)
hexchat.hook_unload(removemenu)

#Add menu items:
hexchat.command('MENU -p-1 ADD HexServ')
hexchat.command('MENU -t1 ADD HexServ/Enabled "hexserv start" "hexserv stop"')
hexchat.command('MENU ADD HexServ/Menu')
hexchat.command('MENU ADD HexServ/-')
hexchat.command('MENU ADD HexServ/About "hexserv"')

#print("{0} module version {1} by {2} loaded.".format(__module_name__, __module_version__, __module_author__))
