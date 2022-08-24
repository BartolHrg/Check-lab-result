import random, time, sys;
r = random.randint(0, 3);
if   r == 0: # correct
	a = int(input());
	b = int(input());
	print(a + b);
	print(a - b);
	print(a * b);
elif r == 1: # incorrect
	print("banana");
elif r == 2: # timeouted
	time.sleep(100);
elif r == 3: # couldn't execute
	print("RNGesus decided this should be an error");
	sys.exit(17);
pass
