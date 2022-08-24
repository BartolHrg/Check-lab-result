# generates tests in cwd
#   ./test{n}/test.in file
#     two integer numbers, separated by newline (\n)
#     a\nb\n
#     %d+\n%d+\n
#   ./test{n}/test.out
#     results of addition (+), subtraction (-), and multiplication (*), separated by newline (\n)
#     a+b\na-b\na*b\n
#     %d+\n%d+\n%d+\n

import os;
import random as rnd;
dir = ".";
for i in range(20):
	subd = os.path.join(dir, f"test{i:02}");
	os.mkdir(subd);
	with \
		open(os.path.join(subd, "test.in"), "w") as fin,  \
		open(os.path.join(subd, "test.out"), "w") as fout \
	:
		a = rnd.randint(-99, 99);
		b = rnd.randint(-99, 99);
		print(a, b, sep="\n", file=fin);
		print(a + b, a - b, a * b, sep="\n", file=fout);
	pass
pass		
