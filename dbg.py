#    pydbg 
#    Copyright (C) 2016 pythonmage
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


from ctypes import *

class dbg :
    def __init__(self) :
        print "bla bla bla"
        self.c=CDLL("/lib/x86_64-linux-gnu/libc.so.6", use_errno=True)
        self.c.ptrace.restype=c_long
        self.c.ptrace.argtypes=[c_long,c_long,c_long,c_long]
        self.c.waitpid.argtypes=[c_long,c_long,c_long]
        self.d = {}
        self.latest = 0
    
    def attach(self, pid) :
        r=self.c.ptrace(16, pid, 0 ,0)
        print(r)
        if(r == -1):
            print get_errno()
        r=self.c.waitpid(pid,0,0x40000000)
        print(r)
        if(r == -1):
            print get_errno()
        r=self.c.ptrace(0x4200, pid, 0, 14)
        print r
        if(r == -1):
            print get_errno()
    
    def detach(self, pid) :
        print(self.c.ptrace(17, pid, 0, 0))
    
    def startbreak(self, pid, di) :
        self.d = di;
        for k in self.d.keys() :
            print(self.c.ptrace(4,pid, k, (self.d[k] & 0xffffffffffffff00) | 0x00000000000000cc))
    
    def contbreaklog(self, pid) :
        #get $rip
        rip = (c_uint64 * 64)()
        print(self.c.ptrace(12, pid, 0, addressof(rip)))
        print "$rip:"
        print rip[16]
        #print self.d
        if (self.d.has_key(rip[16] - 1)) :
            print "addr value:"
            print self.d[rip[16] - 1]
            print(self.c.ptrace(1, pid, rip[16]-1, 0))
            if (self.latest > 0) :
                if (self.d.has_key(self.latest)) :
                    print "poke at latest val:"
                    print (self.d[self.latest] & 0xffffffffffffff00) | 0x00000000000000cc
                    print(self.c.ptrace(4,pid,self.latest,(self.d[self.latest] & 0xffffffffffffff00) | 0x00000000000000cc))
            print "remove breakpoint text"
            print(self.c.ptrace(4,pid,rip[16]-1,self.d[rip[16] - 1]))
            print "decrement rip"
            rip[16] = rip[16] - 1
            print(self.c.ptrace(13,pid,0,addressof(rip)))
            self.latest = rip[16]
    
    def wait(self, pid) :
        curth = self.c.waitpid(pid,0,0x40000000)
        if(curth > 0 & curth < 9000) :
            return curth
        return 0
    
    def trace(self, pid) :
        while True :
            self.curthread = self.wait(pid)
            if (self.curthread > 0) :
                self.contbreaklog(self.curthread)
                print(self.c.ptrace(7,self.curthread,0,0))
            print(self.c.ptrace(7,pid,0,0))

