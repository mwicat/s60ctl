from argh import *

import rpyc
import s60util
import rpycutil
import symbianutil
import sys

CMD_SEP = ' '
HOST_SEP = '#'
PYRUN_RC = r'c:\data\pyrunrc'
PYRUN = 'pyrun_0xe6f08516.exe'

def split_path(path):
    host, path = path.split(HOST_SEP, 1) if HOST_SEP in path else (None, path)
    return host, path

def init_conn(host):
    conn = rpyc.classic.connect(host)
    t = rpyc.BgServingThread(conn)
    return conn
    
@arg('host')
@arg('path')
@arg('args', nargs='*')
def run(args):
    conn = init_conn(args.host)
    command = CMD_SEP.join(args.args)
    s60util.launch(conn, args.path, command)

@command
def copy(src, dst):
    shost, srcfn = split_path(src)
    dhost, dstfn = split_path(dst)
    src_conn = init_conn(shost) if shost else None
    dst_conn = init_conn(dhost) if dhost else None
    rpycutil.rcopy(srcfn, dstfn, src=src_conn, dst=dst_conn)

@command
def install(host, path):
    conn = init_conn(host)
    err = s60util.install(conn, path)

@command
def run_script(host, path):
    conn = init_conn(host)
    f = conn.modules.__builtin__.open(PYRUN_RC, 'w')
    f.write(path)
    f.close()
    s60util.launch(conn, PYRUN)
    
@command
def genuid(name):
    uid = symbianutil.uidfromname(name)
    uidstr = '0x%x' % uid
    yield uidstr

@command
def kill(host, name):
    conn = init_conn(host)
    conn.root.callmain(conn.modules.appswitch.kill_app, unicode(name))    

@command
def shell(host):
    conn = init_conn(host)
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed()
    ipshell(local_ns=locals())

p = ArghParser()
p.add_commands([run, copy, install, genuid, run_script, kill, shell])
p.dispatch()
