#!/usr/bin/env python

# compile lab before using this (except if you use python)

# EDIT this
# no need to edit anything else
using_python = True;   # did you write lab using python
test = "../lab 1 easy/test/";       # folder that contains .in and .out files in itself or its subfolders
if not using_python:
    exe  = '../lab 1 easy/a.exe';   # path to .exe    can be anything if     using_python
else:
    exe  = './testtesta.py' ;   # path to .py     can be anything if not using_python
pass;
in_ext  = '.in' ;       # extension for 'in' files
out_ext = '.out';       # extension for their 'out' files
my_ext  = '.my' ;       # extension for files that program writes to
err_ext = ".err";       #
start_shell_command = "cmd /c ";

# that is an example for the following structure
# + .
# | a.exe
# | + test
# | | + testni primjeri 1
# | | | + test01
# | | | | test01.in
# | | | | test01.out
# | | | + test02
# | | | | test02.in
# | | | | test02.out
# | | + testni primjeri 2
# | | | + test01
# | | | | test01.in
# | | | | test01.out
# | | | + test02
# | | | | test02.in
# | | | | test02.out




import sys, os;

test = os.path.abspath(test);
exe = os.path.abspath(exe);
w = os.walk(test);
next(w);

count = 0;
correct = 0;
couldnt_execute = 0;

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
    fmy  = os.path.commonprefix([fin, fout]);
    if fmy.endswith('.') and my_ext.startswith('.'):
        ferr = fmy + err_ext[1:];
        fmy += my_ext[1:];
    else:
        ferr = fmy + err_ext;
        fmy += my_ext;
    pass;
    
    if not using_python:
        cmd = start_shell_command +         f'"{exe}" < "{fin}" > "{fmy}" 2> "{ferr}"';
    else:
        cmd = start_shell_command + 'py ' + f'"{exe}" < "{fin}" > "{fmy}" 2> "{ferr}"';
    pass;

    if os.system(cmd) == 0:
        count += 1;
        with open(fout) as ffout:
            with open(fmy) as ffmy:
                t1 = ffout.read(); t2 = ffmy.read();
                print(t1 == t2, fin, sep='\t');
                if t1 == t2:
                    correct += 1;
                pass;
            pass;
        pass;
    else:
        couldnt_execute += 1;
        print("couldn't execute");
    pass;
pass;

print();
print(f"correct {correct}/{count}");
if couldnt_execute != 0:
    print(f"failed execution {couldnt_execute} files");
pass;
