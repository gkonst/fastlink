'''
Created on Feb 21, 2009

@author: kostya
'''
import os
import base64
import ConfigParser

from delicious.core.util import log

class LazyConfig(object):

    def __init__(self):
        self._target = None
        
    def __getattr__(self, name):
        if not self._target:
            self._load_config()
        if name == '__members__':
            # Used to implement dir(obj), for example.
            return self._target.get_all_members()
        return getattr(self._target, name)

    def __setattr__(self, name, value):
        if name == '_target':
            # Assign directly to self.__dict__, because otherwise we'd call
            # __setattr__(), which would be an infinite loop.
            self.__dict__['_target'] = value
        else:
            if self._target is None:
                self._load_config()
            setattr(self._target, name, value)
        
    def _load_config(self):
        self._target = Config()
        
    def configure(self):
        self._load_config()
        
    def save(self):
        self._target.save()
        
class Config(object):
    
    def __init__(self):
        log.debug('loading config...')
        home_dir = os.path.expanduser("~")
        self.config_dir = os.path.join(home_dir, ".delicious")
        if not os.path.exists(self.config_dir) or not os.path.isdir(self.config_dir):
            os.mkdir(self.config_dir)
        
        if os.path.exists(os.path.join(self.config_dir, "config")):
            config_parser = ConfigParser.RawConfigParser()
            config_parser.read(os.path.join(self.config_dir, "config"))
            if config_parser.has_option("main", "username"):
                self.username = config_parser.get("main", "username")
                log.debug(' loading username from config : %s', self.username)
            if config_parser.has_option("main", "password"):
                self.password = self._decrypt_password(config_parser.get("main", "password"))
                log.debug(' loading password from config : %s', self.password)
        log.debug('loading config...Ok') 

    def save(self):
        if self.config_dir:
            log.debug("saving config...")
            config_parser = ConfigParser.RawConfigParser()
            config_parser.add_section("main")
            if self.username:
                config_parser.set("main", "username", self.username)
            if self.password:
                config_parser.set("main", "password", self._crypt_password(self.password))
            fo = open(os.path.join(self.config_dir, "config"), "w")
            config_parser.write(fo)
            fo.close()
            log.debug("saving config...Ok")
            
    def _crypt_password(self, password):
        return base64.b64encode(password)
    
    def _decrypt_password(self, password):
        return base64.b64decode(password)
    
    def get_all_members(self):
        return dir(self)
   
config = LazyConfig()
