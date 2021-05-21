#include <stdio.h>
long f(long n) {
    long sl0;
    long sl1;
    long sl2;
    long sl3;
    double sd0;
    double sd1;
    double sd2;
    double sd3;
    char *sc0;
    char *sc1;
    char *sc2;
    char *sc3;
    sl0 = n;
    sl1 = 0;
    sl0 = sl0 == sl1;
    if (!sl0) { goto L12; }
    sl0 = 0;
    return sl0;
L12:;
    sl0 = n;
    sl1 = 1;
    sl0 = sl0 == sl1;
    if (!sl0) { goto L24; }
    sl0 = 1;
    return sl0;
L24:;
    sl1 = n;
    sl2 = 1;
    sl1 = sl1 - sl2;
    sl0 = f(sl1);
    sl2 = n;
    sl3 = 2;
    sl2 = sl2 - sl3;
    sl1 = f(sl2);
    sl0 = sl0 + sl1;
    return sl0;
}
int main(int argc, char *argv[]) {
    long sl0;
    long sl1;
    long sl2;
    long sl3;
    long sl4;
    double sd0;
    double sd1;
    double sd2;
    double sd3;
    double sd4;
    char *sc0;
    char *sc1;
    char *sc2;
    char *sc3;
    char *sc4;
    long loc3;
    sl1 = 50;
L24:;
    long for1 = sl1;
    for (sl1 = 0; sl1 < for1; sl1 += 1) {
        loc3 = sl1;
        sl2 = loc3;
        sl4 = loc3;
        sl3 = f(sl4);
        printf("%ld %ld\n", sl2, sl3);
    }
L44:;
    return 0;
}
