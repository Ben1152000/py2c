#include <stdio.h>

int p(int n) {
  if (n < 4)
    return n > 1;
  if (!((n % 2) && (n % 3)))
    return 0;
  int i = 5;
  while (i * i <= n) {
    if (n % i == 0)
      return 0;
    i += 2;
    if (n % i == 0)
      return 0;
    i += 4;
  }
  return 1;
}

int main(int argc, char* argv[]) {
  int s = 0;
  for (int i = 0; i <= 1000000; ++i) {
    s += p(i);
  }
  printf("%d\n", s);
}
