#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <chrono>

#ifdef _WIN32
	#include <Windows.h>
	#define sleep(seconds) Sleep(seconds * 1000)
#else
	#include <unistd.h>
#endif

int main() {
	// srand((unsigned)time(NULL));
	srand(std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::system_clock::now().time_since_epoch()).count());
	switch (rand() % 4) {
		case 0: { // correct 
			int a, b;
			if (scanf(" %d %d ", &a, &b) != 2) {
				exit(13);
			}
			printf("%d\n%d\n%d\n", a+b, a-b, a*b);
		} break;
		case 1: // incorrect
			printf("cucumber");
		break;
		case 2: // timeouted
			sleep(100);
		break;
		case 3: // couldn't execute
			fprintf(stderr, "RNGesus decided this should be an error");
			exit(17);
		break;
	}
}