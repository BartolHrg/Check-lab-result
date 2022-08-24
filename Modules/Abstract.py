from __future__ import annotations
from typing import *;
from functools import wraps;

import os;
import subprocess;
import contextlib;

def deindentString(str: str) -> str:
	for (i, e) in enumerate(str):
		if not e.isspace(): break;
	pass
	indent = str[ : i];
	if "\n" in indent: indent = indent[indent.rindex("\n") + 1 : ];
	return str.strip().replace("\n"+indent, "\n");
pass

def withStopCheck(f):
	@wraps(f)
	def wrapper(self: Tester, *a, **kw):
		withStopCheck.stopCheck(self);
		r = f(self, *a, **kw);
		withStopCheck.stopCheck(self);
		return r;
	pass
	return wrapper;
pass
def stopCheck(self: Tester):
	if self.should_stop:
		self.should_stop = False;
		raise FinishTest;
	pass
pass
withStopCheck.stopCheck = stopCheck;

TestFileGroup = Any;
class TestControls(Exception): ...
class BreakTest (TestControls): ...
class FinishTest(TestControls): ...
class Tester:
	correct  : int = 0;
	incorrect: int = 0;
	timeouted: int = 0;
	couldnt_execute: int = 0;
	@property
	def total(self): return self.correct + self.incorrect + self.timeouted + self.couldnt_execute;
	
	test_dir: str;
	should_stop: bool = False;
	
	def init(self): ...
	@withStopCheck
	def start(self): ...
	@withStopCheck
	def getFileGroup(self, in_filename: str, exp_filename: str) -> TestFileGroup: ...
	test_files: Iterable[TestFileGroup];
	@withStopCheck
	def callCommand(self, cwd, in_filename, out_filename, err_filename, timeout, args):
		with \
			(open(in_filename)       if in_filename  is not None else contextlib.nullcontext(None)) as in_file,  \
			(open(out_filename, "w") if out_filename is not None else contextlib.nullcontext(None)) as out_file, \
			(open(err_filename, "w") if err_filename is not None else contextlib.nullcontext(None)) as err_file  \
		:
			try:
				return subprocess.run(
					args, 
					stdin=in_file, 
					stdout=out_file, 
					stderr=err_file, 
					cwd=cwd, 
					timeout=timeout, 
					creationflags=subprocess.CREATE_NO_WINDOW
				).returncode;
			except subprocess.TimeoutExpired:
				return "timeout";
			pass
		pass
	pass
	@withStopCheck
	def compareFiles(self, a_name, b_name) -> bool:
		with open(a_name) as a_file, open(b_name) as b_file:
			a = a_file.read();
			b = b_file.read();
			a = a.strip();
			b = b.strip();
			return a == b;
		pass
	pass
	@withStopCheck
	def test(self, file_group: TestFileGroup) -> bool | Literal["timeout", "couldn't execute"]: ...
	@withStopCheck
	def printOneResult(self, r, file_group):
		if r == "couldn't execute":
			self.print("couldn't execute, see", file_group["error"]);
			return;
		pass
		msg = {
			"timeout": "timeout  ",
			True     : "correct  ",
			False    : "incorrect",
		}[r];
		self.print(msg, os.path.relpath(file_group["input"], self.test_dir), sep="   ");
	pass
	@withStopCheck
	def handle(self, ex: Exception) -> Exception | True | None: 
		self.incorrect += 1;
		return True;
	pass
	def finishPrintInfo(self):
		self.print();
		msg = "_" * 150 + "\n" + f"correct {self.correct}/{self.total} (incorrect {self.incorrect}, timeouted {self.timeouted})";
		if self.couldnt_execute != 0:
			msg += f"\nfailed execution of {self.couldnt_execute} files";
		pass
		self.print(msg);
	pass
	def finish(self):
		self.finishPrintInfo();
		self.print('░'*150, '█'*150, sep='\n', end='\n');
		self.correct = self.incorrect = self.timeouted = self.couldnt_execute = 0;
	pass
	def stop(self): self.should_stop = True;

	def main(self: Tester):
		try:
			self.start();

			for file_group in self.test_files:
				try:
					r = self.test(file_group);
					if r == "timeout":
						self.timeouted += 1;
					elif r == "couldn't execute":
						self.couldnt_execute += 1;
					elif r:
						self.correct += 1;
					else:
						self.incorrect += 1;
					pass
				except TestControls:
					raise;		
				except Exception as ex:
					res = self.handle(ex);
					if res == True:
						raise;
					elif res is not None:
						raise res from ex;
					pass
				else:
					self.printOneResult(r, file_group);
				pass
			pass
			self.finish();
		except BreakTest:
			pass;
		except FinishTest:
			self.finish();
		pass
	pass

	def print(self, *args, start="", sep=" ", end="\n"):
		print(start, end=""); print(*args, sep=sep, end=end);
	pass
pass
