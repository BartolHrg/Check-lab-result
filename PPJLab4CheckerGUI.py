from __future__ import annotations;
from typing import *;

from LabCheckerGUI import *;

class PPJLab4CheckerGUI(LabCheckerGUI):
	def getConfigDefaults(self):
		cd = super().getConfigDefaults();
		cd["node.js"] = self.file_selectors["node.js"].var.get();
		cd["main.js"] = self.file_selectors["main.js"].var.get();
		return cd;
	pass

	def defFileTypes(self):
		super().defFileTypes();
		self.file_types["frisc"] = (tk.StringVar(self.window.config_frame, config["defaults"]["extensions"]["frisc"] ),   "frisc",  "frisc source program");
	pass
	def defFileSelectors(self):
		super().defFileSelectors();
		self.file_selectors_data.append(("node.js", False, "path to node.exe or just node if it is on the PATH", config["defaults"]["node.js"]));
		self.file_selectors_data.append(("main.js", False, "path to main.js that is used to run frisc",            config["defaults"]["main.js"]));
	pass

	def start(self):
		self.nodejs_var = self.file_selectors["node.js"].var;
		self.mainjs_var = self.file_selectors["main.js"].var;
		super().start();
	pass

	def getFileGroup(self, in_filename: str, exp_filename: str) -> TestFileGroup:
		fg = super().getFileGroup(in_filename, exp_filename);
		(a, bc) = os.path.split(fg["frisc"]);
		(b, c) = os.path.splitext(bc);
		fg["frisc"] = os.path.join(a, "a" + c);
		return fg;
	pass

	def test(self, file_group):
		self.window.window.update();
		r = self.callCommand(
			os.path.dirname(file_group["input"]),
			file_group["input"],
			None, # file_group["frisc"],
			file_group["error"],
			self.timeout_var.get(),
			self.args,
		);
		if r == "timeout":
			return r;
		elif r != 0:
			return "couldn't execute";
		pass
		r = self.callCommand(
			os.path.dirname(file_group["input"]),
			None,
			file_group["output"],
			file_group["error"],
			self.timeout_var.get(),
			[self.nodejs_var.get(), self.mainjs_var.get(), file_group["frisc"]],
		);
		if r == "timeout":
			return r;
		elif r != 1:
			return "couldn't execute";
		pass
		if self.use_delay_var.get(): time.sleep(self.delay_var.get());
		r = self.compareFiles(
			file_group["expected"],
			file_group["output"],
		);
		return r;
	pass
pass

if __name__ == '__main__':
	print('Py__' * 20)

	t = PPJLab4CheckerGUI();
	t.init();
	t.mainloop();

	print('Py==' * 20)
pass
