import sys, os;

import json;

_path = os.path.join(os.path.dirname(__file__), "../config.json");
with open(_path) as _file:
	config = json.load(_file);
pass

def saveConfig(config):
	with open(_path) as _to_save:
		_save = _to_save.read();
	pass
	try:
		with open(_path, "w") as _file:
			json.dump(config, _file, indent="\t");
		pass
	except:
		with open(_path, "w") as _to_save:
			_to_save.write(_save);
		pass
		raise;
	pass
pass
