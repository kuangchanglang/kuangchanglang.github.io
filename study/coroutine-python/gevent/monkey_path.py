def patch_all(socket=True, dns=True, time=True, select=True, thread=True, os=True, 
                ssl=True, httplib=False, subprocess=True, sys=False,
                aggressive=True, Event=False, builtins=True, signal=True)
"""
        Do all of the default monkey patching 
        (calls every other applicable function in this module).
"""
