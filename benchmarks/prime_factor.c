#include <stdio.h>
long f(long n) {
    long sl0;
    long sl1;
    double sd0;
    double sd1;
    char *sc0;
    char *sc1;
    long fasloc1;
    sl0 = 2;
    fasloc1 = sl0;
L4:;
    sl0 = fasloc1;
    sl1 = fasloc1;
    sl0 = sl0 * sl1;
    sl1 = n;
    sl0 = sl0 <= sl1;
    if (!sl0) { goto L48; }
L16:;
    sl0 = n;
    sl1 = fasloc1;
    sl0 = sl0 % sl1;
    sl1 = 0;
    sl0 = sl0 == sl1;
    if (!sl0) { goto L38; }
    sl0 = n;
    sl1 = fasloc1;
    sl0 = sl0 / sl1;
    n = sl0;
L36:;
    goto L16;
L38:;
    sl0 = fasloc1;
    sl1 = 1;
    sl0 = sl0 + sl1;
    fasloc1 = sl0;
L46:;
    goto L4;
L48:;
    sl0 = n;
    return sl0;
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
    long loc0;
    sl0 = 100128601319183;
    loc0 = sl0;
    sl2 = loc0;
    sl1 = f(sl2);
    printf("%ld\n", sl1);
    return 0;
}
