'''
Created on Jan 14, 2011

@author: Administrator
'''

import Queue

inst_queue = Queue.Queue()

def inst_cb(err):
    inst_queue.put(err)

def install(conn, path):
    conn.root.install(path, inst_cb)
    err = inst_queue.get()
    return err

def launch(conn, path, command=''):
    e32 = conn.modules.e32
    e32.start_exe(unicode(path), command)