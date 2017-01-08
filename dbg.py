#    pydbg 
#    Copyright (C) 2016-2017 pythonmage
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
import ctypes.util

class dbg :
    def __init__(self) :
        print "initializing the puthon debugger"
        self.c=CDLL(ctypes.util.find_library("c"), use_errno=True)
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
            print(self.c.ptrace(4,pid, k, (self.d[k] & 0xffffffff00000000) | 0x00000000fedeffe7))
    
    def contbreaklog(self, pid) :
        #get $rip
        rip = (c_long * 64)()
        print(self.c.ptrace(12, pid, 0, addressof(rip)))
        print "$rip:"
        print rip[15]
        for i in range(0, 18):
            print rip[i]
        #print self.d
        if (self.d.has_key(rip[15])) :
            print "addr value:"
            print self.d[rip[15]]
            print(self.c.ptrace(1, pid, rip[15], 0))
            if (self.latest > 0) :
                if (self.d.has_key(self.latest)) :
                    print "poke at latest val:"
                    print (self.d[self.latest] & 0xffffffff00000000) | 0x00000000fedeffe7
                    print(self.c.ptrace(4,pid,self.latest,(self.d[self.latest] & 0xffffffff00000000) | 0x00000000fedeffe7))
            print "remove breakpoint text"
            print(self.c.ptrace(4,pid,rip[15],self.d[rip[15]]))
            print "decrement rip"
            rip[15] = rip[15]
            print(self.c.ptrace(13,pid,0,addressof(rip)))
            self.latest = rip[15]
    
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
            else :
                print(self.c.ptrace(7,pid,0,0))

