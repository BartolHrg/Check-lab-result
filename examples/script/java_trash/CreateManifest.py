import sys;
name=sys.argv[1];
with open(name+".mf", "w") as f:
	f.write("Manifest-Version: 1.0\nMain-Class: " + name + "\n");
pass
