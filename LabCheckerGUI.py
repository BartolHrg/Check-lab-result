from __future__ import annotations
from typing import *;

import traceback;

from Modules.Abstract import *;
from Modules.GUIComponents import *

class LabCheckerGUI(Tester):
	window: MainWindow;
	language_chooser: LanguageChooser;
	file_selectors: dict[str, FileInput];
	file_types: dict[str, tuple[tk.Variable, str, str]];
	timeout: InputWithLabels;
	delay: TimeDelay;
	run_only_one_test: tk.BooleanVar;
	controls: Controls;
	output: Output;
	
	is_running = False;
	
	def init(self):
		self.window = window = MainWindow();
		window.init();
		window.title = self.__class__.__name__ + " " + config["version"];
		config_frame = window.config_frame;
		
		
		self.language_chooser = LanguageChooser(); 
		self.language_chooser.init(config_frame);
		tmp = tk.Frame(config_frame);
		HelpButton().init(tmp, deindentString("""
			Well, you've chosen a wrong language, use C# next time.
			Unlike in other languages, running things is complicated with Java.
			If you have Java version greater or equal to 11, you can run it from source.
			    If you have single .java file in your project just run it.
			    If there are more, 
			        first compile project with javac, but don't use ./bin/ folder,
					(.class files should be each in the same folder as source file)
			        and then run it (put .java file with main method in "your program" field).
			You can compile to EXECUTABLE jar (you can search online how to do it, I don't know, I don't use inferior language like Java)
			Lastly, you can make custom script for running your java
		"""), "Help for inferior language users", "Help for Java users");
		for child in tmp.children.values(): child['bg'] = "orange";
		tmp.pack(fill=tk.X);
		del tmp;
		self.defFileSelectors();
		self.file_selectors = {};
		for x in self.file_selectors_data: 
			self.file_selectors[x[0]] = _fi = FileInput();
			_fi.init(config_frame, *x);
		pass
		self.defFileTypes();
		FileTypes().init(self.window.config_frame, *self.file_types.values());
		self.timeout = InputWithLabels();
		self.timeout.init(config_frame, "timeout", "seconds", lambda: tk.DoubleVar(config_frame, config["defaults"]["timeout"]), "in case there is infinite loop, terminate program when time exceedes limit");
		self.delay = TimeDelay();
		self.delay.init(config_frame);
		tmp = tk.Frame(config_frame);
		self.run_only_one_test = run_only_one_test = tk.BooleanVar(config_frame, config["defaults"]["run one"]);
		tk.Checkbutton(tmp, text="Run only one test?", variable=run_only_one_test).pack(side=tk.LEFT);
		tmp.pack(fill=tk.X);
		del tmp;
		tmp = tk.Frame(config_frame);
		tk.Button(tmp, text="Save config defaults", command=self.saveConfigDefaults).pack(side=tk.LEFT);
		tmp.pack(fill=tk.X);
		del tmp;
		
		self.controls = Controls();
		self.controls.init(window.controls_frame, self);
		
		self.output = Output();
		self.output.init(window.out_frame);
	pass
	def getConfigDefaults(self):
		return {
			"test folder": self.file_selectors["Test folder" ].var.get(),
			"program":     self.file_selectors["your program"].var.get(),
			"lang": self.language_chooser.var.get(),
			"extensions": { t: v.get() for (t, (v, *_)) in self.file_types.items() },
			"timeout": self.timeout.var.get(),
			"delay": {
				"use": self.delay.cond.get(),
				"amount": self.delay.time.get(),
			},
			"run one": self.run_only_one_test.get(),
			
			# "node.js": "node.js",
			# "main.js": "./main.js"
		};
	pass
	def saveConfigDefaults(self):
		if not dialog.askyesno("Save Config defaults", "Save Config defaults"): return;
		# config["defaults"] = self.getConfigDefaults();
		def recursiveExtendDict(dst: dict, src: dict):
			for (key, value) in src.items():
				if isinstance(value, dict):
					recursiveExtendDict(dst.setdefault(key, {}), value);
				else:
					dst[key] = value;
				pass
			pass
		pass
		recursiveExtendDict(config["defaults"], self.getConfigDefaults());				
		saveConfig(config);
	pass

	def defFileTypes(self):
		self.file_types = {
			"input"   : (tk.StringVar(self.window.config_frame, config["defaults"]["extensions"]["input"   ]),   "input files",  "program input"),
			"expected": (tk.StringVar(self.window.config_frame, config["defaults"]["extensions"]["expected"]),   "their output", "expected output, will not be modified"),
			"output"  : (tk.StringVar(self.window.config_frame, config["defaults"]["extensions"]["output"  ]),   "your output",  "output file, will be modified, will be created if doesn't exist"),
			"error"   : (tk.StringVar(self.window.config_frame, config["defaults"]["extensions"]["error"   ]),   "error output", "file for writing errors, will be modified, will be created if doesn't exist"),
		}
	pass
	def defFileSelectors(self):
		self.file_selectors_data = [
			("Test folder",  True,  deindentString("""
				folder that contains .in and .out files
				in itself or its subfolders
				or their subfolders, and so on
			"""), config["defaults"]["test folder"]),
			("your program", False, deindentString("""
				your program (compile it before testing)
				In case of Python: .py file
				In case of script: .ps1, .cmd, .bat, .sh file
				In case of Java: .java or .jar file (see "Help for Java users")
			"""), config["defaults"]["program"]),
		];
	pass

	def start(self):
		try:
			self.lang_var = self.language_chooser.var;
			self.test_folder_var = self.file_selectors["Test folder" ].var;
			self.program_var     = self.file_selectors["your program"].var;
			self.file_types_vars = { t: v for (t, (v, *_)) in self.file_types.items() };
			self.timeout_var = self.timeout.var;
			self.use_delay_var = self.delay.cond;
			self.delay_var     = self.delay.time;
		except:
			self.print("problem with the variables", end="_"*10 + "\n");
			self.print(traceback.format_exc());
			raise BreakTest;
		pass
		self.exe = self.program_var.get();
		if not os.path.exists(self.exe):
			if not dialog.askyesno("File doesn't exist!", f"Error: {self.exe} doesn't exist\nContinue anyway?"):
				raise BreakTest;
			pass
		pass
		self.exe = os.path.abspath(self.exe);
		self.test_dir = self.test_folder_var.get();
		if not os.path.exists(self.test_dir):
			if not dialog.askyesno("File doesn't exist!", f"Error: {self.test_dir} doesn't exist\nContinue anyway?"):
				raise BreakTest;
			pass
		pass
		self.test_dir = os.path.abspath(self.test_dir);
		self.args = self.language_chooser.get_cmd([self.exe]);
		if self.args is None: raise BreakTest;
		self.print(f"running {self.exe}", f"on test folder {self.test_dir}", start='░'*150+'\n', sep='\n', end='\n'+'_'*150+'\n'); 
	pass
	
	def getFileExtensions(self):
		self.file_extensions = { key: var.get() for (key, var) in self.file_types_vars.items() };
	pass
	def getFileGroup(self, in_filename: str, exp_filename: str) -> TestFileGroup:
		pref   = os.path.commonprefix([in_filename, exp_filename]);
		def appendExtension(pref: str, ext: str) -> str:
			c = (pref.endswith(".") << 1) | ext.startswith(".");
			if   c == 0b11:
				pref = pref[ : -1];
			elif c == 0b00:
				pref += "."; # THIS MIGHT BE BAD
			pass
			return pref + ext;
		pass
		self.last_file_group = { key: appendExtension(pref, ext) for (key, ext) in self.file_extensions.items() };
		return self.last_file_group;
	pass
	@property
	def test_files(self): yield from self._test_files_generator();
	def _test_files_generator(self):
		self.getFileExtensions();
		walk = os.walk(self.test_dir);
		for (folder, _, files) in walk:
			withStopCheck.stopCheck(self);
			fin = fexp = None;
			for file in files:
				if file.endswith(self.file_extensions["input"]):
					fin = file;
				pass
				if file.endswith(self.file_extensions["expected"]):
					fexp = file;
				pass
			pass
			if fin is None or fexp is None:
				continue;
			pass
			fin    = os.path.join(folder, fin);
			fexp   = os.path.join(folder, fexp);
			yield self.getFileGroup(fin, fexp);
			withStopCheck.stopCheck(self);
		pass
	pass

	def test(self, file_group):
		self.window.window.update();
		r = self.callCommand(
			os.path.dirname(file_group["input"]),
			file_group["input"],
			file_group["output"],
			file_group["error"],
			self.timeout_var.get(),
			self.args,
		);
		if r == "timeout":
			return r;
		elif r != 0:
			return "couldn't execute";
		pass
		if self.use_delay_var.get(): time.sleep(self.delay_var.get());
		r = self.compareFiles(
			file_group["expected"],
			file_group["output"],
		);
		return r;
	pass
	def printOneResult(self, r, file_group):
		super().printOneResult(r, file_group);
		self.window.window.update();
		if self.run_only_one_test.get():
			raise FinishTest;
		pass
	pass
	
	def handle(self, ex: Exception) -> Exception | True | None: return super().handle(ex);
	
	def finish(self):
		n_tests = self.total;
		super().finish();
		if config["warn about single test"] and n_tests == 1:
			dialog.showwarning("Careful!", deindentString('''
				You only run 1 test file!
				There might be more
				Uncheck "Run only one test?"
			'''));
		pass
	pass

	def main(self: Tester):
		if self.is_running: return;
		self.is_running = True;
		try:
			super().main();
		except:
			self.print(traceback.format_exc());
		pass
		self.is_running = False;
	pass

	def mainloop(self):
		if config["use tkinter mainloop"]:
			self.window.window.mainloop();
		pass
	pass

	def print(self, *args, start="", sep=" ", end="\n"):
		stdout = sys.stdout;
		sys.stdout = self.output;
		super().print(*args, start=start, sep=sep, end=end);
		sys.stdout = stdout;
	pass
pass


if __name__ == '__main__':
	print('Py__' * 20)

	t = LabCheckerGUI();
	t.init();
	t.mainloop();

	print('Py==' * 20)
pass
