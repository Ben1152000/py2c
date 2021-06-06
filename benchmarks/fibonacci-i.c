#include <stdio.h>

int f(int n) {
  if (n == 0) {
    return 0;
  }
  if (n == 1) {
    return 1;
  } else {
    return f(n - 1) + f(n - 2);
  }
}

int main(int argc, char *argv[]) {
  for (int i = 0; i < 35; ++i) {
    printf("%d %d\n", i, f(i));
  }
}
