import os
import json
import sys
import argparse
from .utils import get_config_path, raise_error
from .info import (
    __appname__,
    __description__,
)

root = os.path.abspath(os.path.dirname(__file__))+"/"

class ConfigManager(object):
    def __init__(self):
        self.config=dict()
        self.load_default()
        self.config_dir = get_config_path()
        self.config_file = os.path.join(self.config_dir,"settings.json")

    def load_default(self):
        self.config = {
            "default_theme": "auto",
            "theme_path": [os.path.join(root,"themes")],
            "default_delay": 1,
            "min_delay": 0.1,
            "retries": 3,
            "user_agant": "",
            "output_path": ".",
            "output_format": "{title}",
            "symlink_static": False
        }

    def load_usercfg(self):
        if not os.path.isdir(self.config_dir):
            return
        try:
            with open(os.path.join(self.config_dir,self.config_file),"r") as f:
                conf=json.load(f)
            self.config.update(self.verify_config(conf))
        except json.decoder.JSONDecodeError as e:
            raise_error("Config load error: "+e.msg)

    def save_usercfg(self):
        if not os.path.isdir(self.config_dir):
            os.mkdir(self.config_dir)
            os.mkdir(os.path.join(self.config_dir,"themes"))
            self.config["theme_path"]+=[os.path.join(self.config_dir,"themes")]
        with open(self.config_file,"w") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def generate_theme_option(self,args=sys.argv):
        parser=argparse.ArgumentParser(prog=__appname__.lower(),description=__description__)

    def verify_config(self,sd):

        for key in sd:
            if key not in self.config:
                sd.pop(key)
            elif type(sd[key]) != type(self.config[key]):
                sd.pop(key)

        theme_paths=self.config['theme_path']
        for path in sd.get('theme_path'):
            if not os.path.isdir(path):
                sd['theme_path'].remove(path)
            theme_paths.append(path)

        valid_themes=["auto"]
        [valid_themes.append(j) for i in theme_paths for j in os.listdir(i) if not j.startswith('.') and not j in valid_themes]

        rules_dict = {
            "default_theme": valid_themes,
        }

        for key, valid_values in list(rules_dict.items()):
            if sd[key] not in valid_values:
                sd.pop(key)

        dd=self.config['default_delay']
        if sd.get('default_delay'):
            if sd['default_delay']<0:
                sd.pop('default_delay')
            else:
                dd=sd['default_delay']
        if sd.get('min_delay'):
            if sd['min_delay']<0 or sd['min_delay'] > dd:
                sd.pop('min_delay')

        if sd.get('retries') and sd.get('retries') < 0:
            sd.pop('min_delay')

        if sd.get('output_format'):
            try:
                sd['output_format'].format("",ncode="",title="")
            except:
                sd.pop('output_format')
        return sd

class ArgumentManager(object):
    def __init__(self):
        pass