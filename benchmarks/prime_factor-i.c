#include <stdio.h>

int f(long n) {
  int i = 2;
  while (i * i <= n) {
    while (n % i == 0) {
      n /= i;
    }
    ++i;
  }
  return n;
}

int main(int argc, char *argv[]) {
  long n = (long)(10006428 + 1) * (long)(10006428 - 1);
  printf("%d\n", f(n));
}
