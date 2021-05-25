#include <stdio.h>
long p(long n) {
    long sl0;
    long sl1;
    long sl2;
    double sd0;
    double sd1;
    double sd2;
    char *sc0;
    char *sc1;
    char *sc2;
    long fasloc1;
    long fasloc2;
    sl0 = 0;
    fasloc1 = sl0;
    sl1 = 1;
    sl2 = n;
L14:;
    long for0 = sl1;
    long for1 = sl2;
    for (long for3 = for0; for3 < for1; for3 += 1) {
        sl1 = for3;
        fasloc2 = sl1;
        sl1 = n;
        sl2 = fasloc2;
        sl1 = sl1 % sl2;
        if (sl1) { goto L34; }
        sl1 = fasloc1;
        sl2 = fasloc2;
        sl1 = sl1 + sl2;
        fasloc1 = sl1;
    L34:;
    }
L36:;
    sl1 = fasloc1;
    sl2 = n;
    sl1 = sl1 == sl2;
    return sl1;
}
int main(int argc, char *argv[]) {
    long sl0;
    long sl1;
    long sl2;
    double sd0;
    double sd1;
    double sd2;
    char *sc0;
    char *sc1;
    char *sc2;
    long loc4;
    sl1 = 10000;
L24:;
    long for1 = sl1;
    for (long for3 = 0; for3 < for1; for3 += 1) {
        sl1 = for3;
        loc4 = sl1;
        sl2 = loc4;
        sl1 = p(sl2);
        if (!sl1) { goto L44; }
        sl2 = loc4;
        printf("%ld\n", sl2);
    L44:;
    }
L46:;
    return 0;
}
