#include <stdio.h>

int c(long n) {
  int i = 0;
  while (n > 1) {
    if (n % 2 == 0) {
      n >>= 1;
    } else {
      n *= 3;
      n++;
    }
    i++;
  }
  return i;
}

int main(int argc, char *argv[]) {
  int l = 1;
  int m = 0;
  int n = 1000000;
  for (int i = 0; i < n; ++i) {
    int a = c(i);
    if (a > m) {
      m = a;
      l = i;
    }
  }
  printf("%d\n", l);
}
