#include <stdio.h>

int p(int n) {
  int s = 0;
  for (int i = 1; i < n; ++i) {
    if (n % i == 0) {
      s += i;
    }
  }
  return s == n;
}

int main(int argc, char *argv[]) {
  for (int i = 0; i < 10000; ++i) {
    if (p(i)) {
      printf("%d\n", i);
    }
  }
}
