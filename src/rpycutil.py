'''
Created on Jan 13, 2011

@author: Administrator
'''

from shutil import copyfileobj
import os

def _open(conn, fn, mode='r'):
    openf = open if conn is None else conn.modules.__builtin__.open
    return openf(fn, mode)

def rcopyfileobj(srcfn, dstfn, src=None, dst=None):
    return copyfileobj(_open(src, srcfn, 'rb'), _open(dst, dstfn, 'wb'))
    
def rcopy(srcfn, dstfn, src=None, dst=None):
    isdirf = os.path.isdir if dst is None else dst.modules.os.path.isdir
    if isdirf(dstfn):
        dstfn = os.path.join(dstfn, os.path.basename(srcfn))
    return rcopyfileobj(srcfn, dstfn, src, dst)
