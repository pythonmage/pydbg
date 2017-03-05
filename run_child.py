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

import subprocess
from dbg import *

def run_child(child):
    subprocess.Popen(child)

def test():
    run_child("./tests/nativeapp")

class Tests:
    def pre_run(self):
        subprocess.


    def test_break(self):
        test()
        self.pid = int(subprocess.check_output(["/bin/sh","-c", "ps ax | grep nativeapp"]).split()[0])
        self.d=dbg()
        self.d.attach(self.pid)
        self.addr1 = int("0x" + subprocess.check_output(["/bin/sh","-c", "nm ./tests/nativeapp | grep function1"]).split()[0], base=16)
        self.val1=c_ulong(self.d.c.ptrace(1,self.pid,self.addr1,0)).value
        self.d.setBreakpoint(self.pid, self.addr1,self.val1)
        self.d.c.ptrace(7,self.pid,0,0)
        self.d.contbreaklog(self.pid)
    
    def test_twoBreakpointsAndContBreakLog(self):
        test()
        self.pid = int(subprocess.check_output(["/bin/sh","-c", "ps ax | grep nativeapp"]).split()[0])
        self.d=dbg()
        self.d.attach(self.pid)
        self.addr1 = int("0x" + subprocess.check_output(["/bin/sh","-c", "nm ./tests/nativeapp | grep function1"]).split()[0], base=16)
        self.addr2 = int("0x" + subprocess.check_output(["/bin/sh","-c", "nm ./tests/nativeapp | grep function2"]).split()[0], base=16)
        self.val1=c_ulong(self.d.c.ptrace(1,self.pid,self.addr1,0)).value
        self.val2=c_ulong(self.d.c.ptrace(1,self.pid,self.addr2,0)).value
        self.d.setAllBreakpoints(self.pid, {self.addr1:self.val1,self.addr2:self.val2})
        self.d.c.ptrace(7,self.pid,0,0)
        self.d.contbreaklog(self.pid)
        self.d.contbreaklog(self.pid)
        self.d.contbreaklog(self.pid)
        print("pass")

        

