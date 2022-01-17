#!/usr/bin/env python

import sys, os, subprocess, time;
import tkinter as tk, tkinter.ttk as ttk, tkinter.filedialog as tkfiles, tkinter.messagebox as dialog;

# compile lab before using this (except if you use python)

window = tk.Tk(); 
window.geometry("1500x600");

############# defaults ###############################################################################

lang = ".py";     # language that you have written in

test_var = tk.StringVar(window, "C:/Personal/nastava/5. semestar/Prevodjenje programskih jezika/lab/lab 4/TEST/");                # folder that contains .in and .out files in itself or its subfolders

exe_var  = tk.StringVar(window, "C:/Personal/nastava/5. semestar/Prevodjenje programskih jezika/lab/lab 4/TEST/primjer/pr.py");   # path to your COMPILED executable (or source if .py or others)

node_var    = tk.StringVar(window, "node");                      # path to your node.js executable
main_js_var = tk.StringVar(window, "C:/Personal/nastava/5. semestar/Prevodjenje programskih jezika/lab/lab 4/main.js");                              # path to main.js with which you run frisc

in_ext_var     = tk.StringVar(window, ".in" );             # extension for 'in' files
out_ext_var    = tk.StringVar(window, ".out");             # extension for their 'out' files
my_ext_var     = tk.StringVar(window, ".my" );             # extension for files that program writes to
frisc_ext_var  = tk.StringVar(window, ".frisc" );          # extension for frisc assembly files
err_ext_var    = tk.StringVar(window, ".err");             # errors

#                                                         # one person had problem that his output was red before it was writen to a file
using_time_sleep = tk.BooleanVar(window, False);          # set this to True if the results are `False` and you've checked that .my and .out file are identical
time_sleep_time = tk.DoubleVar(window, 0.5)               # 0.5 seconds


run_only_one_test = tk.BooleanVar(window, False);	    # run only one test and exit

# that is an example for the following structure
# + .
# | + test
# | | test.py (this file)
# | + lab1
# | | a.exe
# | | a.py
# | | + test
# | | | + testni primjeri 1
# | | | | + test01
# | | | | | test01.in
# | | | | | test01.out
# | | | | + test02
# | | | | | test02.in
# | | | | | test02.out
# | | | + testni primjeri 2
# | | | | + test01
# | | | | | test01.in
# | | | | | test01.out
# | | | | + test02
# | | | | | test02.in
# | | | | | test02.out

config_frame = tk.LabelFrame(window, text="config");
config_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=5, pady=5);

class FileInput:
	def __init__(self, label, var: tk.Variable, folder: bool, help) -> None:
		frame = tk.Frame(config_frame);
		frame.pack(fill=tk.X);
		self.label = label;
		self.var = var;
		self.ask = tkfiles.askdirectory if folder else tkfiles.askopenfilename;
		tk.Label(frame, text=label).pack(side=tk.LEFT);
		tk.Entry(frame, textvariable=var ).pack(side=tk.LEFT, expand=True, fill=tk.X);
		tk.Button(frame, text="select", command=self.cmd).pack(side=tk.LEFT);
		tk.Button(frame, text="help", command=self.help).pack(side=tk.LEFT);
		self.helpmsg = help;
	pass;
	def cmd(self):
		a = self.ask(initialdir=os.path.dirname(self.var.get()) or ".");
		if a is not None and a != "":
			self.var.set(a);
		pass;
	pass;
	def help(self):
		dialog.showinfo(f"help on {self.label}", self.helpmsg);
	pass;
pass;
class LanguageChooser:
	options = {
		".py": lambda args: [sys.executable, *args],
		".exe": lambda args: args,
		".java": lambda args: dialog.showerror("Error", "Java not supported") and False or None,
	};
	def __init__(self) -> None:
		frame = tk.Frame(config_frame);
		frame.pack(fill=tk.X);
		self.var = tk.StringVar(frame, lang);
		for opt in LanguageChooser.options:
			tk.Radiobutton(frame, text=opt, value=opt, variable=self.var).pack(side=tk.LEFT);
		pass;
	pass;
	def get_cmd(self, args):
		return LanguageChooser.options[self.var.get()](args);
	pass;
pass;
class FileTypes:
	def __init__(self, *args) -> None:
		frame = tk.Frame(config_frame);
		frame.pack(fill=tk.X);
		for ext, label in args:
			area = tk.Frame(frame);
			area.pack(side=tk.LEFT);
			tk.Label(area, text=label, anchor=tk.W).pack(fill=tk.X);
			tk.Entry(area, textvariable=ext)           .pack(fill=tk.X);
		pass;
	pass;
pass;
class TimeDelay:
	def __init__(self, cond: tk.BooleanVar, time: tk.DoubleVar) -> None:
		self.cond = cond;
		self.time = time;
		frame = tk.Frame(config_frame);
		frame.pack(fill=tk.X);
		tk.Checkbutton(frame, variable=cond, text="Use time delay?", command=self.disenable).pack(side=tk.LEFT);
		self.entry = tk.Entry(frame, textvariable=time);
		self.entry.pack(side=tk.LEFT);
		tk.Button(frame, text="help", command=self.help).pack(side=tk.LEFT);
		self.disenable();
	pass;
	def disenable(self):
		self.entry["state"] = tk.NORMAL if self.cond.get() else tk.DISABLED;
	pass;	
	def help(self):
		dialog.showinfo("Help on time delay", "Someone had a problem, where outputs were compared\nbefore output was written to .my file.\nThis will delay this many seconds before comparing");
	pass;
pass;

class RunTests:
	def __init__(self) -> None:
		frame = tk.Frame(window);
		frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=5, pady=5);
		tk.Button(frame, text="run tests",    command=RunTests.runTests).pack(side=tk.LEFT);
		tk.Button(frame, text="clear output", command=RunTests.clear   ).pack(side=tk.LEFT);
	pass;
	@staticmethod
	def clear():
		output["state"] = tk.NORMAL;
		output.delete(0.0, tk.END);
		output["state"] = tk.DISABLED;
	pass;
	@staticmethod
	def runTests():
		test = os.path.abspath(test_var.get());
		exe = os.path.abspath(exe_var.get());

		if not os.path.exists(exe):
			if not dialog.askyesno("File doesn't exist!", f"Error: {exe} doesn't exist\nContinue anyway?"):
				sys.exit(1);
			pass;
		pass;
		if not os.path.exists(test):
			if not dialog.askyesno("File doesn't exist!", f"Error: {test} doesn't exist\nContinue anyway?"):
				sys.exit(1);
			pass;
		pass;

		path_to_node    =    node_var.get();
		path_to_main_js = main_js_var.get();
		
		in_ext    =    in_ext_var.get();
		out_ext   =   out_ext_var.get();
		my_ext    =    my_ext_var.get();
		frisc_ext = frisc_ext_var.get();
		err_ext   =   err_ext_var.get();

		args = lang.get_cmd([exe]);
		if args is None:
			return;
		pass;

		print(f"running {exe}", f"on test folder {test}", start='_'*150+'\n', sep='\n', end='\n'+'_'*150+'\n');

		w = os.walk(test);

		count = 0;
		correct = 0;
		couldnt_execute = 0;
		try:
			for folder, _, files in w:
				fin = fout = None;
				for file in files:
					if file.endswith(in_ext):
						fin = file;
					pass;
					if file.endswith(out_ext):
						fout = file;
					pass;
				pass;
				if fin is None or fout is None:
					continue;
				pass;
				fin  = os.path.join(folder, fin);
				fout = os.path.join(folder, fout);
				ffrisc = os.path.commonprefix([fin, fout]);
				fmy    = os.path.commonprefix([fin, fout]);
				if ffrisc.endswith('.') and frisc_ext.startswith('.'):
					ffrisc += frisc_ext[1:];
				else:
					ffrisc += frisc_ext;
				pass;
				if fmy.endswith('.') and my_ext.startswith('.'):
					ferr = fmy + err_ext[1:];
					fmy += my_ext[1:];
				else:
					ferr = fmy + err_ext;
					fmy += my_ext;
				pass;

				with open(fin) as ffin, open(ffrisc, 'w') as fffrisc, open(fmy, 'w') as ffmy, open(ferr, 'w') as fferr:
					if subprocess.run(args, stdin=ffin, stdout=fffrisc, stderr=fferr).returncode != 0:
						print("couldn't compile, see", ferr);
						couldnt_execute += 1;
						if run_only_one_test.get():
							break;
						else:
							continue;
						pass;
					pass;
					if subprocess.run([path_to_node, path_to_main_js, ffrisc], stdout=ffmy, stderr=fferr).returncode != 1: # main.js uvijek vraća 1?
						print("couldn't execute, see", ferr);
						couldnt_execute += 1;
						if run_only_one_test.get():
							break;
						else:
							continue;
						pass;
					pass;
				pass;

				count += 1;
				if using_time_sleep.get():
					time.sleep(time_sleep_time.get());
				pass;

				with open(fmy) as ffmy, open(fout) as ffout:
					tmy = ffmy.read(); tout = ffout.read(); 
					print("correct  " if tmy == tout else "incorrect", fin, sep='\t', end='\n');
					if tmy == tout:
						correct += 1;
					pass;
				pass;
				
				if run_only_one_test.get():
					break;
				pass;
			pass;
		except:
			print();
			msg = "Error!!!!!!!!!!!!\nCurrent state:\n";
			try:
				msg += f"{args=}\n";
			except NameError:
				pass;
			pass;
			try:
				msg += f"{exe=}\n";
			except NameError:
				pass;
			pass;
			try:
				msg += f"{test=}\n";
			except NameError:
				pass;
			pass;
			try:
				msg += f"{folder=}\n";
			except NameError:
				pass;
			pass;
			try:
				msg += f"{fin=}\n";
			except NameError:
				pass;
			pass;
			try:
				msg += f"{fout=}\n";
			except NameError:
				pass;
			pass;
			print(msg);
		else:
			print();
			msg = f"\ncorrect {correct}/{count}";
			if couldnt_execute != 0:
				msg += f"\nfailed execution of {couldnt_execute} files";
			pass;
			print(msg);
			dialog.showinfo("Result", msg);
			if count == 1:
				dialog.showwarning("Careful!", 'You only run 1 test file!\nThere might be more\nUncheck "Run only one test?"');
			pass;
		finally:
			print('#'*150, sep='\n', end='\n');
		pass;
	pass;
pass;

lang = LanguageChooser();
FileInput("Test folder",  test_var,    True,  "folder that contains .in and .out files\nin itself or its subfolders\nor their subfolders, and so on");
FileInput("your program", exe_var,     False, "your program (compile it before testing)\n");
FileInput("node.js",      node_var,    False, "path to your node.js executable\n");
FileInput("main.js",      main_js_var, False, "path to your main.js that runs frisc\n");
FileTypes(
	(in_ext_var,    "input files"), 
	(out_ext_var,   "their output"),
	(my_ext_var,    "your output"),
	(frisc_ext_var, "frisc assembly"),
	(err_ext_var,   "error output"),
);
TimeDelay(using_time_sleep, time_sleep_time)
tmp = tk.Frame(config_frame);
tk.Checkbutton(tmp, text="Run only one test?", variable=run_only_one_test).pack(side=tk.LEFT);
tmp.pack(fill=tk.X);
del tmp;
tk.Button(window, text="Quit tkinter mainloop", command=window.quit).pack();

RunTests();

out_frame = tk.Frame(window);
out_frame.pack(expand=True, fill=tk.BOTH);
output = tk.Text(out_frame, wrap=tk.NONE); # output.insert(0.0, lorem_ipsum);
yscroll = tk.Scrollbar(out_frame, orient=tk.VERTICAL  , command=output.yview, ); yscroll.grid(row=2, column=3, sticky=tk.NS); output['yscrollcommand'] = yscroll.set;
xscroll = tk.Scrollbar(out_frame, orient=tk.HORIZONTAL, command=output.xview, ); xscroll.grid(row=3, column=2, sticky=tk.EW); output['xscrollcommand'] = xscroll.set;
output.grid(row=2, column=2, sticky=tk.NSEW);
out_frame.rowconfigure   (2, weight=1);
out_frame.columnconfigure(2, weight=1);

def print(*args, start="", sep=' ', end="\n"+"_"*150+"\n"):
	sep = str(sep);
	x = str(start);
	if args:
		first, *args = args;
		x += str(first);
		for arg in args:
			x += sep;
			x += str(arg);
		pass;
	pass;
	x += str(end);
	output["state"] = tk.NORMAL;
	output.insert(tk.END, x);
	output["state"] = tk.DISABLED;
	output.update();
	output.see(tk.END);
pass;

window.mainloop();

lorem_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus vehicula dolor tristique dictum luctus. Aliquam erat volutpat. 
Aenean finibus bibendum ornare. Sed semper sem eget suscipit consectetur. Suspendisse at dui at nunc lobortis fermentum. 
Nam congue mauris suscipit, rhoncus justo eget, ullamcorper nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; 
Cras sit amet tortor egestas, ultricies risus nec, vulputate orci. Nullam sit amet augue fringilla, viverra purus at, bibendum dolor. 
Nullam tincidunt, ex ultricies scelerisque lobortis, tortor enim accumsan sem, nec porttitor leo sapien eu nisl. 
Proin suscipit, neque non porta condimentum, turpis risus convallis diam, et pretium metus augue in tellus. Etiam blandit felis sapien, id ullamcorper lectus tempus non.

Cras quis turpis tellus. Donec ultricies ultrices consectetur. Integer ut velit elementum sapien vulputate consequat. 
Curabitur volutpat dictum nisl in laoreet. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam cursus augue in elit luctus, ut placerat massa luctus. 
Sed eleifend sapien nec nibh fermentum, lobortis vulputate lorem ullamcorper.

Vestibulum sit amet laoreet libero. Etiam non ligula nisi. In rhoncus faucibus congue. Mauris dictum nisl massa, vel consectetur risus consectetur a. 
Vivamus eget nulla at arcu pellentesque sodales. Integer id ullamcorper arcu. Vivamus accumsan ullamcorper quam, quis porttitor leo finibus sit amet. 
Duis ultrices maximus mauris facilisis bibendum. Pellentesque nec ligula pharetra, luctus augue vel, sagittis justo. Quisque lacinia laoreet dolor et tincidunt. 
Maecenas nisi velit, viverra quis neque id, blandit pulvinar diam. Quisque nec porta ante, quis tempor sapien. Donec ut ultrices tortor, nec volutpat diam.

Vestibulum finibus mattis tempus. In in egestas arcu. Integer gravida et est sed efficitur. Maecenas in justo sagittis, pulvinar felis ac, pharetra elit. 
Etiam a nibh aliquam, scelerisque purus ac, pulvinar elit. Aenean ac orci quis velit ultrices malesuada. Sed congue vehicula elit, in venenatis nisl fermentum feugiat. 
Nam nec sem tincidunt, semper risus eget, ultrices enim. Donec suscipit mollis dignissim. Quisque porta feugiat erat, quis imperdiet lacus finibus et. 
Interdum et malesuada fames ac ante ipsum primis in faucibus. Quisque faucibus sollicitudin nunc non scelerisque. Nulla iaculis vel augue et mattis. 
Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Fusce pharetra vel diam ac eleifend. Nullam tempus, massa non posuere gravida, lectus ligula suscipit sapien, in mollis eros ex ac velit. 
Etiam ipsum nunc, fermentum et blandit vitae, maximus eu justo. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. 
Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nulla id augue eu ex ullamcorper ullamcorper. 
Sed et justo condimentum, sagittis tellus vel, semper erat. Ut eget arcu nulla. Vestibulum gravida ipsum felis, vitae rutrum nisl condimentum eget. 
Nunc nec tincidunt nulla. Nam non lacus nec nisl gravida molestie. Etiam in massa ac urna scelerisque hendrerit. Aenean a posuere lacus, pellentesque aliquam lorem. 
Donec euismod, magna lobortis tempor ultricies, quam ligula porttitor felis, in vehicula risus velit sit amet ante.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus vehicula dolor tristique dictum luctus. Aliquam erat volutpat. 
Aenean finibus bibendum ornare. Sed semper sem eget suscipit consectetur. Suspendisse at dui at nunc lobortis fermentum. 
Nam congue mauris suscipit, rhoncus justo eget, ullamcorper nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; 
Cras sit amet tortor egestas, ultricies risus nec, vulputate orci. Nullam sit amet augue fringilla, viverra purus at, bibendum dolor. 
Nullam tincidunt, ex ultricies scelerisque lobortis, tortor enim accumsan sem, nec porttitor leo sapien eu nisl. 
Proin suscipit, neque non porta condimentum, turpis risus convallis diam, et pretium metus augue in tellus. Etiam blandit felis sapien, id ullamcorper lectus tempus non.

Cras quis turpis tellus. Donec ultricies ultrices consectetur. Integer ut velit elementum sapien vulputate consequat. 
Curabitur volutpat dictum nisl in laoreet. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam cursus augue in elit luctus, ut placerat massa luctus. 
Sed eleifend sapien nec nibh fermentum, lobortis vulputate lorem ullamcorper.

Vestibulum sit amet laoreet libero. Etiam non ligula nisi. In rhoncus faucibus congue. Mauris dictum nisl massa, vel consectetur risus consectetur a. 
Vivamus eget nulla at arcu pellentesque sodales. Integer id ullamcorper arcu. Vivamus accumsan ullamcorper quam, quis porttitor leo finibus sit amet. 
Duis ultrices maximus mauris facilisis bibendum. Pellentesque nec ligula pharetra, luctus augue vel, sagittis justo. Quisque lacinia laoreet dolor et tincidunt. 
Maecenas nisi velit, viverra quis neque id, blandit pulvinar diam. Quisque nec porta ante, quis tempor sapien. Donec ut ultrices tortor, nec volutpat diam.

Vestibulum finibus mattis tempus. In in egestas arcu. Integer gravida et est sed efficitur. Maecenas in justo sagittis, pulvinar felis ac, pharetra elit. 
Etiam a nibh aliquam, scelerisque purus ac, pulvinar elit. Aenean ac orci quis velit ultrices malesuada. Sed congue vehicula elit, in venenatis nisl fermentum feugiat. 
Nam nec sem tincidunt, semper risus eget, ultrices enim. Donec suscipit mollis dignissim. Quisque porta feugiat erat, quis imperdiet lacus finibus et. 
Interdum et malesuada fames ac ante ipsum primis in faucibus. Quisque faucibus sollicitudin nunc non scelerisque. Nulla iaculis vel augue et mattis. 
Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Fusce pharetra vel diam ac eleifend. Nullam tempus, massa non posuere gravida, lectus ligula suscipit sapien, in mollis eros ex ac velit. 
Etiam ipsum nunc, fermentum et blandit vitae, maximus eu justo. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. 
Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nulla id augue eu ex ullamcorper ullamcorper. 
Sed et justo condimentum, sagittis tellus vel, semper erat. Ut eget arcu nulla. Vestibulum gravida ipsum felis, vitae rutrum nisl condimentum eget. 
Nunc nec tincidunt nulla. Nam non lacus nec nisl gravida molestie. Etiam in massa ac urna scelerisque hendrerit. Aenean a posuere lacus, pellentesque aliquam lorem. 
Donec euismod, magna lobortis tempor ultricies, quam ligula porttitor felis, in vehicula risus velit sit amet ante.

"""

