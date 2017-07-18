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
        print "initializing the python debugger"
        self.c=CDLL(ctypes.util.find_library("c"), use_errno=True)
        self.c.ptrace.restype=c_long
        self.c.ptrace.argtypes=[c_long,c_long,c_long,c_long]
        self.c.waitpid.argtypes=[c_long,c_long,c_long]
        self.d = {}
        self.latest = 0
        self.arch="armv7"
        self.pc_offset = 16
        if self.arch == "armv7":
            print("Arch is " + self.arch)
            self.pc_offset = 15
    
    def attach(self, pid) :
        r = self.c.ptrace(16, pid, 0, 0)
        if(r == -1):
            print get_errno()
        r = self.c.waitpid(pid, 0, 0x40000000)
        if(r == -1):
            print get_errno()
        r = self.c.ptrace(0x4200, pid, 0, 14)
        if(r == -1):
            print get_errno()
    
    def detach(self, pid) :
        print(self.c.ptrace(17, pid, 0, 0))
    
    def setBreakpoint(self, pid, address, wordAtAddress) :
        self.d[address] = wordAtAddress
        if self.arch == "armv7":
            return self.c.ptrace(4,pid, address, (wordAtAddress & 0xffffffff00000000) | 0x00000000fedeffe7)
        else:
            return self.c.ptrace(4,pid, address, (wordAtAddress & 0xffffffffffffff00) | 0x00000000000000cc)
    
    def clearBreakpoint(pid, address) :
        self.c.ptrace(4,pid,address,self.d[address])
    
    def setAllBreakpoints(self, pid, di) :
        for k in di.keys() :
            print(self.setBreakpoint(pid, k, di[k]))
    
    def contbreaklog(self, pid) :
        #get reg_set
        reg_set = (c_long * 64)()
        r = self.c.ptrace(12, pid, 0, addressof(reg_set))
        if r == -1:
            print r
            print get_errno()
        print("$ip:")
        print(hex(reg_set[self.pc_offset]))
        for i in range(0, 18):
            print(hex(reg_set[i]))
        #find $ip in self.d dictionary
        if (self.d.has_key(reg_set[self.pc_offset])) :
            print("addr value:")
            print(hex(self.d[reg_set[self.pc_offset]]))
            print(hex(self.c.ptrace(1, pid, reg_set[self.pc_offset], 0)))
            #re-add latest breakpoint at address self.latest. It was cleared at the previous continue.
            if (self.latest > 0) :
                if (self.d.has_key(self.latest)) :
                    print "poke at latest val:"
                    print (self.d[self.latest] & 0xffffffff00000000) | 0x00000000fedeffe7
                    print(self.c.ptrace(4,pid,self.latest,(self.d[self.latest] & 0xffffffff00000000) | 0x00000000fedeffe7))
            #clear breakpoint and continue
            print "remove breakpoint text near $ip"
            print(self.c.ptrace(4,pid,reg_set[self.pc_offset],self.d[reg_set[self.pc_offset]]))
            print "decrement $ip"
            if self.arch == "x86" or self.arch =="x86_64":
                reg_set[self.pc_offset] = reg_set[self.pc_offset] - 1
            print(self.c.ptrace(13,pid,0,addressof(reg_set)))
            self.latest = reg_set[self.pc_offset]
            print "continue"
            print(self.c.ptrace(7,pid,0,0))
    
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
            else :
                print(self.c.ptrace(7,pid,0,0))

