#include <stdio.h>

int main(int argc, char* argv[]) {
  long s = 0;
  int n = 10000000;
  for (int i = 0; i < n; ++i) {
    s += i;
  }
  printf("%d %ld\n", n, s);
}
