#include <stdio.h>
long t(long c, long p) {long sl0;
long sl1;
long sl2;
long sl3;
long sl4;
long sl5;
double sd0;
double sd1;
double sd2;
double sd3;
double sd4;
double sd5;
char* sc0;
char* sc1;
char* sc2;
char* sc3;
char* sc4;
char* sc5;
long fasloc2;
long fasloc3;
long fasloc4;
sl0 = 0;
fasloc2 = sl0;
sl1 = c;
L12:;
long for1 = sl1;
for (long for3 = 0; for3 < for1; for3 += 1) {
sl1 = for3;
fasloc3 = sl1;
sl2 = c;
L24:;
long for5 = sl2;
for (long for7 = 0; for7 < for5; for7 += 1) {
sl2 = for7;
fasloc4 = sl2;
sl2 = fasloc3;
sl3 = fasloc3;
sl2 = sl2 * sl3;
sl3 = fasloc4;
sl4 = fasloc4;
sl3 = sl3 * sl4;
sl2 = sl2 + sl3;
sl3 = c;
sl4 = c;
sl3 = sl3 * sl4;
sl2 = sl2 == sl3;
if(!sl2){
goto L76;
}
sl2 = p;
if(!sl2){
goto L68;
}
sl3 = fasloc3;
sl4 = fasloc4;
sl5 = c;
printf("%ld %ld %ld\n", sl3, sl4, sl5);
L68:;
sl2 = fasloc2;
sl3 = 1;
sl2 = sl2 + sl3;
fasloc2 = sl2;
L76:;
}
L78:;
}
L80:;
sl2 = fasloc2;
return sl2;
}
int main(int argc, char* argv[]){
long sl0;
long sl1;
long sl2;
long sl3;
double sd0;
double sd1;
double sd2;
double sd3;
char* sc0;
char* sc1;
char* sc2;
char* sc3;
long loc3;
long loc4;
long loc5;
long loc7;
long loc8;
sl0 = 500;
loc3 = sl0;
sl0 = 0;
loc4 = sl0;
sl0 = 0;
loc5 = sl0;
sl1 = loc3;
sl2 = 1;
sl1 = sl1 + sl2;
L42:;
long for1 = sl1;
for (long for3 = 0; for3 < for1; for3 += 1) {
sl1 = for3;
loc7 = sl1;
sl2 = loc7;
sl3 = 0;
sl1 = t(sl2, sl3);
loc8 = sl1;
sl1 = loc8;
sl2 = loc5;
sl1 = sl1 > sl2;
if(!sl1){
goto L72;
}
sl1 = loc7;
loc4 = sl1;
sl1 = loc8;
loc5 = sl1;
L72:;
}
L74:;
sl2 = loc4;
sl3 = 1;
sl1 = t(sl2, sl3);
return 0;
}
