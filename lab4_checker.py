#!/usr/bin/env python

import sys, os, subprocess, time;

# compile lab before using this (except if you use python)

# EDIT this
# no need to edit anything else

run_only_one_test = False;					# run only one test and exit

test = "../lab 4/test";		# folder that contains .in and .out files in itself or its subfolders or their subfolders

using_python = False;				# did you write lab in python
if not using_python:
    exe  = '../lab 4/a.exe';	# path to .exe    can be anything if     using_python
    exe = os.path.abspath(exe);
    args = [exe];
else:
    exe  = '../lab 4/a.py';		# path to .py     can be anything if not using_python
    exe = os.path.abspath(exe);
    args = [sys.executable, exe]; # try also with ['powershell', '/C', sys.executable, exe]
pass

path_to_node = "node"; # node is in $PATH probably
path_to_main_js = "../lab 4/main.js";

in_ext  = '.in' ;					# extension for 'in' files
out_ext = '.out';					# extension for their 'out' files
frisc_ext  = '.frisc' ;					# extension for FRISC files 
my_ext  = '.my' ;					# extension for files that program writes to
err_ext = ".err";					# errors

using_time_sleep = False;       # one person had problem that his output was red before it was writen to a file
                                # set this to True if the results are `False` and you've checked that .my and .out file are identical
time_sleep_time = 0.5           # 0.5 seconds
    
# that is an example for the following structure
# + .
# | + test
# | | test.py (this file)
# | + lab 4
# | | a.exe
# | | a.py
# | | main.js
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




path_to_main_js = os.path.abspath(path_to_main_js);
test = os.path.abspath(test);
exe = os.path.abspath(exe);

if not os.path.exists(exe):
    print(f"Error: {exe} doesn't exist", end=' ');
    if input("continue (yes/no)? ") != "yes":
        sys.exit(1);
    pass
    print("continuing");
pass
if not os.path.exists(test):
    print(f"Error: {test} doesn't exist", end=' ');
    if input("continue (yes/no)? ") != "yes":
        sys.exit(1);
    pass
    print("continuing");
pass
if not os.path.exists(path_to_main_js):
    print(f"Error: {path_to_main_js} doesn't exist", end=' ');
    if input("continue (yes/no)? ") != "yes":
        sys.exit(1);
    pass
    print("continuing");
pass

print(f"running {exe}");
print(f"on test folder {test}");
print();

w = os.walk(test);
# next(w);

count = 0;
correct = 0;
couldnt_execute = 0;
try:
    for folder, _, files in w:
        fin = fout = None;
        for file in files:
            if file.endswith(in_ext):
                fin = file;
            pass
            if file.endswith(out_ext):
                fout = file;
            pass
        pass
        if fin is None or fout is None:
            continue;
        pass
        fin  = os.path.join(folder, fin);
        fout = os.path.join(folder, fout);
        ffrisc = os.path.commonprefix([fin, fout]);
        fmy    = os.path.commonprefix([fin, fout]);
        if ffrisc.endswith('.') and frisc_ext.startswith('.'):
            ffrisc += frisc_ext[1:];
        else:
            ffrisc += frisc_ext;
        pass
        if fmy.endswith('.') and my_ext.startswith('.'):
            ferr = fmy + err_ext[1:];
            fmy += my_ext[1:];
        else:
            ferr = fmy + err_ext;
            fmy += my_ext;
        pass

        with open(fin) as ffin, open(ffrisc, 'w') as fffrisc, open(fmy, 'w') as ffmy, open(ferr, 'w') as fferr:
            if subprocess.run(args, stdin=ffin, stdout=fffrisc, stderr=fferr).returncode != 0:
                print("couldn't compile, see", ferr);
                couldnt_execute += 1;
                if run_only_one_test:
                    break;
                else:
                    continue;
                pass
            pass
            if subprocess.run([path_to_node, path_to_main_js, ffrisc], stdout=ffmy, stderr=fferr).returncode != 0 and False: # main.js uvijek vraća 1?
                print("couldn't execute, see", ferr);
                couldnt_execute += 1;
                if run_only_one_test:
                    break;
                else:
                    continue;
                pass
            pass
        pass

        count += 1;
        if using_time_sleep:
            time.sleep(time_sleep_time);
        pass

        with open(fmy) as ffmy, open(fout) as ffout:
            tmy = ffmy.read(); tout = ffout.read();
            print(tmy.strip() == tout.strip(), fin, sep='\t');
            if tmy.strip() == tout.strip():
                correct += 1;
            pass
        pass
        
        if run_only_one_test:
            break;
        pass
    pass
except:
    print("Error");
    print("current state: ");
    try:
        print(f"{args=}");
    except NameError:
        pass
    pass
    try:
        print(f"{exe=}");
    except NameError:
        pass
    pass
    try:
        print(f"{test=}");
    except NameError:
        pass
    pass
    try:
        print(f"{folder=}");
    except NameError:
        pass
    pass
    try:
        print(f"{fin=}");
    except NameError:
        pass
    pass
    try:
        print(f"{fout=}");
    except NameError:
        pass
    pass
    raise;
else:
    print();
    print(f"correct {correct}/{count}");
    if couldnt_execute != 0:
        print(f"failed execution {couldnt_execute} files");
    pass
pass
