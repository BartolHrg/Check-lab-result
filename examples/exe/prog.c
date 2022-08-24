#include <stdio.h>
#include <stdlib.h>

int main() {
	int a, b;
	if (scanf(" %d %d ", &a, &b) != 2) {
		exit(13);
	}
	printf("%d\n%d\n%d\n", a+b, a-b, a*b);
}