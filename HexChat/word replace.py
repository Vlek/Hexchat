import hexchat

__module_name__ = 'Word Replace'
__module_version__ = '0.0.1'
__module_description__ = 'Replaces words with others'
__module_author__ = 'Vlek'

"""
Just change what replacements you'd like in here.
You could have it set to allow for a command that enables editing
but you'd also have to save the information into the plugin's config.
It was a lot more effort than a simple script to call Drakonis a dildo
called for. ;)
"""
_replacements = {'drakonis':'dildos', 'irc':'life'}


def check_for_replacements(word, word_to_eol, userdata):
    global _replacements
    result = []
    changed = False
    for w in word[1].split():
        w = w.lower()
        if w in _replacements.keys():
            result.append(_replacements[w])
            changed = True
        else:
            result.append(w)
    if changed:
        if len(word) == 2:
            word.append('')
        hexchat.get_context().emit_print('Channel Message', word[0], ' '.join(result), word[2])
        return hexchat.EAT_ALL

hexchat.hook_print('Channel Message', check_for_replacements, priority=hexchat.PRI_LOW)
hexchat.hook_print('Channel Msg Hilight', check_for_replacements, priority=hexchat.PRI_LOW)
