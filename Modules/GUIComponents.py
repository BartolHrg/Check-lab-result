from __future__ import annotations;
from typing import *;

import os, sys, subprocess, time;
import tkinter as tk, tkinter.ttk as ttk, tkinter.filedialog as tkfiles, tkinter.messagebox as dialog


from .Abstract import *;
from .Config import *;

class MainWindow:
	window: tk.Tk;
	config_frame: tk.Widget;
	controls_frame: tk.Widget;
	out_frame: tk.Widget;
	
	@property
	def title(self): return self.window.title();
	@title.setter
	def title(self, value): self.window.title(value);
	
	def init(self):
		self.window = tk.Tk();
		self.window.geometry(config["window dimensions"]);
		self.config_frame = tk.LabelFrame(self.window, text="config");
		self.config_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=5, pady=5);
		tk.Button(self.window, text="Quit tkinter mainloop", command=self.window.quit).pack();
		self.controls_frame = tk.Frame(self.window);
		self.controls_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=5, pady=5);
		self.out_frame = tk.Frame(self.window);
		self.out_frame.pack(expand=True, fill=tk.BOTH);
	pass
pass
class HelpButton:
	def init(self, frame, msg, title="help", label="help"):
		self.msg = msg;
		self.title = title;
		tk.Button(frame, text=label, command=self.cmd, background="aqua").pack(side=tk.LEFT, padx=5);
	pass
	def cmd(self):
		dialog.showinfo(self.title, self.msg);
	pass
pass
class FileInput:
	def init(self, frame, label, folder: bool, help, default=".") -> None:
		self.var = var = tk.StringVar(frame, default);
		frame = tk.Frame(frame);
		frame.pack(fill=tk.X);
		self.var = var;
		self.ask = tkfiles.askdirectory if folder else tkfiles.askopenfilename;
		HelpButton().init(frame, help, f"help on {label}");
		tk.Button(frame, text="select", command=self.cmd).pack(side=tk.LEFT);
		tk.Label(frame, text=label).pack(side=tk.LEFT);
		tk.Entry(frame, textvariable=var ).pack(side=tk.LEFT, expand=True, fill=tk.X);
		self.helpmsg = help;
	pass
	def cmd(self):
		a = self.ask(initialdir=os.path.dirname(self.var.get()) or ".");
		if a is not None and a != "":
			self.var.set(a);
		pass
	pass
pass
class LanguageChooser:
	options = {
		".py":    lambda args: [sys.executable, *args],
		".exe":   lambda args: args,
		"script": lambda args: args,
		".java":  lambda args: ["java", *args],
		".jar":   lambda args: ["java", "-jar", *args], # [*args[0].split(maxsplits=1), *args[1:]], # [tkfiles.askopenfilename(title="script that runs your java")]
	};
	def init(self, frame) -> None:
		frame = tk.Frame(frame);
		frame.pack(fill=tk.X);
		self.var = tk.StringVar(frame, config["defaults"]["lang"]);
		# frame.after(2000, lambda *_: self.var.set(config["defaults"]["lang"]));
		HelpButton().init(frame, deindentString("""
			choose language (in which you have written)
			if it is compiled to exe (you have to compile it), choose .exe
			if you write your own script to run a program use script (see script_example.sh)
			if you use java (also, see "Help for Java users")
			    and have jvm version ≥ 11, you can use .java
			    else compile to EXECUTABLE jar and use .jar
			    or use script
		"""), "Help on Language Chooser");
		for opt in LanguageChooser.options:
			tk.Radiobutton(frame, text=opt, value=opt, variable=self.var).pack(side=tk.LEFT);
		pass
	pass
	def get_cmd(self, args):
		return LanguageChooser.options[self.var.get()](args);
	pass
pass
class FileTypes:
	def init(self, frame, *args) -> None:
		frame = tk.LabelFrame(frame, text="file extensions");
		frame.pack(fill=tk.X);
		HelpButton().init(frame, deindentString("""
			these are file EXTENSIONS used for testing
			you should have input file and expected output provided by your professor(s)
		""") + "\n\n" + "\n".join(label + ": " + description for (var, label, description) in args), "Help on File Types");
		for (ext, label, description) in args:
			area = tk.Frame(frame);
			area.pack(side=tk.LEFT);
			tk.Label(area, text=label, anchor=tk.W).pack(fill=tk.X);
			tk.Entry(area, textvariable=ext)       .pack(fill=tk.X);
		pass
	pass
pass
class TimeDelay:
	def init(self, frame) -> None:
		frame = tk.Frame(frame);
		frame.pack(fill=tk.X);
		self.cond = tk.BooleanVar(frame, config["defaults"]["delay"]["use"]);
		self.time = tk.DoubleVar(frame, config["defaults"]["delay"]["amount"]);
		HelpButton().init(frame, deindentString("""
			Someone had a problem, where outputs were compared
			before output was written to .my file.
			This will delay comparison this many seconds
		"""), "Help on time delay");
		tk.Checkbutton(frame, variable=self.cond, text="Use time delay?", command=self.disenable).pack(side=tk.LEFT);
		self.entry = tk.Entry(frame, textvariable=self.time);
		self.entry.pack(side=tk.LEFT);
		tk.Label(frame, text="seconds").pack(side=tk.LEFT);
		# tk.Button(frame, text="help", command=self.help).pack(side=tk.LEFT);
		self.disenable();
	pass
	def disenable(self):
		self.entry["state"] = tk.NORMAL if self.cond.get() else tk.DISABLED;
	pass	
pass
class InputWithLabels:
	def init(self, frame, before_label: str, after_label, Var: Callable[[], tk.Variable], help=None):
		self.var = Var();
		frame = tk.Frame(frame);
		frame.pack(fill=tk.X);
		if help is not None: HelpButton().init(frame, help, f"help on {before_label}");
		tk.Label(frame, text=before_label).pack(side=tk.LEFT);
		self.entry = tk.Entry(frame, textvariable=self.var);
		self.entry.pack(side=tk.LEFT);
		tk.Label(frame, text=after_label).pack(side=tk.LEFT);
	pass
pass
class Controls:
	tester: Tester;
	def init(self, frame, tester):
		self.tester = tester;
		tk.Button(frame, text="run tests",    command=self.runTests, background="light green").pack(side=tk.LEFT);
		tk.Button(frame, text="clear output", command=self.clear                             ).pack(side=tk.LEFT);
		tk.Button(frame, text="stop",         command=self.breakOut                          ).pack(side=tk.LEFT);
		self.stop = False;
	pass
	def breakOut(self): self.tester.stop(); # TODO: `raise FinishTest;` doesn't work
	def clear(self):
		# self.tester.output.output["state"] = tk.NORMAL;
		self.tester.output.output.delete(0.0, tk.END);
		# self.tester.output.output["state"] = tk.DISABLED;
	pass
	def runTests(self): self.tester.main();
pass
class Output:
	def init(self, frame):
		self.output = output = tk.Text(frame, wrap=tk.NONE); # output.insert(0.0, lorem_ipsum);
		yscroll = tk.Scrollbar(frame, orient=tk.VERTICAL  , command=output.yview, ); yscroll.grid(row=2, column=3, sticky=tk.NS); output['yscrollcommand'] = yscroll.set;
		xscroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=output.xview, ); xscroll.grid(row=3, column=2, sticky=tk.EW); output['xscrollcommand'] = xscroll.set;
		output.grid(row=2, column=2, sticky=tk.NSEW);
		frame.rowconfigure   (2, weight=1);
		frame.columnconfigure(2, weight=1);
	pass
	def write(self, str): 
		self.output.insert(tk.END, str);
		if config["scroll with output"]: self.output.see(tk.END);
	pass
pass
