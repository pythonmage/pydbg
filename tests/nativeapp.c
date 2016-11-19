/*
    pydbg 
    Copyright (C) 2016 pythonmage

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
*/

#include "unistd.h"
#include "stdio.h"

void testfunction1() {

  printf("testfunction1 trace\n");
  sleep(1);
}

void testfunction2() {

  printf("testfunction2 trace\n");
  sleep(1);
}

void testfunction3() {

  printf("testfunction3 trace\n");
  sleep(1);
}


int main(int argc, char *argv[]) {

  while (1) {
    //
    testfunction1();
    testfunction2();
    testfunction3();
    fflush(stdout);
  }
  
  return 0;
}
