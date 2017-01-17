#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import os
import sys

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.config
import lib.constants

if(os.path.exists(lib.constants.slave_slaveconst_dir)):
  sys.path.append(lib.constants.slave_slaveconst_dir)

import glob
import platform

class slaveconst(object):
  def __init__(self):
    self.__retdict = self.__get_preset_consts()
    self.__userconst = self.__update_slaveconst()
    self.__retdict.update(self.__userconst)


  def slaveconst(self):
    return(self.__retdict)


  def __get_preset_consts(self):
    retdict = {}
    retdict['hostname'] = lib.constants.ip
    retdict['ip'] = lib.constants.hostname
    retdict['platform'] = platform.system()
    retdict['architecture'] = platform.architecture()
    retdict['os'] = platform.dist()
    return(retdict)

  def __update_slaveconst(self):
    userconsts = {}
    if (os.path.exists(lib.constants.slave_slaveconst_dir)):
      pyfiles = glob.glob(os.path.join(lib.constants.slave_slaveconst_dir, "*.py"))
      if (pyfiles):
        for x in pyfiles:
          module_to_load = ".".join(x.split(os.sep)[-1].split(".")[:-1])
          module_consts = {}
          exec ("import " + module_to_load)
          exec ("module_consts = " + module_to_load + ".update_consts()")
          if (module_consts):
            userconsts.update(module_consts)
          del module_to_load

    return (userconsts)




if __name__ == '__main__':
  consts = slaveconst()
  print(consts.slaveconst())