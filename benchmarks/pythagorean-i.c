#include <stdio.h>

int t(int c, int p) {
  int n = 0;
  for (int a = 0; a < c; ++a) {
    for (int b = 0; b < c; ++b) {
      if (a * a + b * b == c * c) {
        if (p)
          printf("%d %d %d\n", a, b, c);
        n++;
      }
    }
  }
  return n;
}

int main(int argc, char* argv[]) {
  int n = 500;
  int l = 0;
  int m = 0;
  for (int i = 0; i <= n; ++i) {
    int a = t(i, 0);
    if (a > m) {
      l = i;
      m = a;
    }
  }
  t(l, 1);
}
