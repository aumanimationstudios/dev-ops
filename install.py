#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import argparse
import subprocess
import appdirs
import yaml


os.environ['XDG_CONFIG_DIRS'] = '/etc'
configdir = os.path.join(appdirs.site_config_dir(),"dev-ops")
masterdir = os.path.join(configdir,"master")
slavedir = os.path.join(configdir,"slave")


supervisorpath = "/etc/supervisor/conf.d/"
installdir = "/opt/dev-ops"
states_path = "/srv/dev-ops/states/"
events_root = "/srv/dev-ops/events/"
masterconst_root = "/srv/dev-ops/masterconst/"

progpath = installdir
source_master_path = os.path.join(progpath,"install","master")
source_slave_path = os.path.join(progpath,"install","slave")
installed_slave_conf = os.path.join(slavedir,"slave.conf")
slave_supervisorconf = os.path.join(progpath,"install","supervisor","slave")
master_supervisorconf = os.path.join(progpath,"install","supervisor","master")
print(progpath)

parser = argparse.ArgumentParser()
parser.add_argument("--slave",dest="slave",action="store_true",help="install config files for slave")
parser.add_argument("--groups",dest="groups",help="add the slave to comma seperated groups or a single group")
parser.add_argument("--master",dest="master",action="store_true",help="install config files for master")
args = parser.parse_args()


gitclone = "cd /opt/ ; git clone https://github.com/shrinidhi666/dev-ops.git ;cd /opt/dev-ops; git checkout master; cd -"
gitpull =  "cd /opt/dev-ops/ ; git pull"

def gitupdate():
  p = subprocess.Popen(gitpull,shell=True,stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  output = p.communicate()
  print (output)
  ret = p.wait()
  return(ret)

def gitnew():
  p = subprocess.Popen(gitclone,shell=True,stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  output = p.communicate()
  print (output)
  ret = p.wait()
  return(ret)


if(args.master):
  if(os.path.exists(installdir)):
    ret = gitupdate()
  else:
    ret = gitnew()

  if(ret):
    sys.exit(1)


  try:
    os.makedirs(masterdir)
  except:
    print(sys.exc_info())


  try:
    os.makedirs(states_path)
  except:
    print(sys.exc_info())

  try:
    os.makedirs(events_root)
  except:
    print(sys.exc_info())

  try:
    os.makedirs(masterconst_root)
  except:
    print(sys.exc_info())

  try:
    os.system("rsync -av "+ source_master_path.rstrip(os.sep) +"/ "+ masterdir.rstrip(os.sep) +"/")
  except:
    print(sys.exc_info())

  try:
    os.system("rsync -av "+ master_supervisorconf.rstrip(os.sep) +"/ "+ supervisorpath.rstrip(os.sep) +"/")
  except:
    print(sys.exc_info())


if(args.slave):
  if (os.path.exists(installdir)):
    ret = gitupdate()
  else:
    ret = gitnew()

  if (ret):
    sys.exit(1)

  try:
    os.makedirs(slavedir)
  except:
    print(sys.exc_info())

  try:
    os.system("rsync -av "+ source_slave_path.rstrip(os.sep) +"/ "+ slavedir.rstrip(os.sep) +"/")
  except:
    print(sys.exc_info())

  try:
    os.system("rsync -av "+ slave_supervisorconf.rstrip(os.sep) +"/ "+ supervisorpath.rstrip(os.sep) +"/")
  except:
    print(sys.exc_info())

  if(args.groups):
    sc_fd = open(installed_slave_conf,"r")
    slave_conf_dict = yaml.safe_load(sc_fd)
    sc_fd.close()
    slave_conf_dict['slave_group'] = args.groups
    sc_fd = open(installed_slave_conf, "w")
    yaml.dump(slave_conf_dict, sc_fd, default_flow_style=False)
    sc_fd.flush()
    sc_fd.close()








