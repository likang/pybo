# -*- encoding:utf-8 -*-
import os,sys,ConfigParser

class Config:
  file_path = '~/.pybo'

  def __init__(self, section):
    self.__section__ = section
    self.app_id  = 3743872231 
    self.width   = 80
    self.username = ''
    self.password = ''
    self.access_token  = ''
    self.token_expires = 0

    self.load()
  
  def load(self):
    cp = self.__get_config_parser()

    for key,value in self.__dict__.items:
      if key.startswith('__'):  continue
      if not cp.has_option(self.__section__, key):  continue

      if type(value).__name__ == 'int':
        try:  setattr(self, key, cp.getint(self.__section__, key))
        except: 
          print "invalid option '%s' of section %s in file: %s" % (key, self.__section__, self.file_path)
          sys.exit(2)
      setattr(self, key) == cp.get(self.__section__, key)

  def write_back(self):
    cp = self.__get_config_parser()
    if not cp.has_section(self.__section__):
      cp.add_section(self.__section__)
    for key,value in self.__dict__.items:
      if key.startswith('__'):  continue
      cp.set(self.__section__, key, value)

    full_path = os.path.expanduser(self.file_path)
    f = open(full_path, 'w')
    cp.write(f)
    f.close()

  def __get_config_parser(self):
    full_path = os.path.expanduser(self.file_path)
    cp = ConfigParser.ConfigParser()
    cp.read(full_path)
    return cp
