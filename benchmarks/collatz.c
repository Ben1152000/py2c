#include <stdio.h>
long c(long n) {long sl0;
long sl1;
double sd0;
double sd1;
char* sc0;
char* sc1;
long fasloc1;
sl0 = 0;
fasloc1 = sl0;
L4:;
sl0 = n;
sl1 = 1;
sl0 = sl0 > sl1;
if(!sl0){
goto L60;
}
sl0 = n;
sl1 = 2;
sl0 = sl0 % sl1;
sl1 = 0;
sl0 = sl0 == sl1;
if(!sl0){
goto L34;
}
sl0 = n;
sl1 = 2;
sl0 = sl0 / sl1;
n = sl0;
goto L50;
L34:;
sl0 = n;
sl1 = 3;
sl0 = sl0 * sl1;
n = sl0;
sl0 = n;
sl1 = 1;
sl0 = sl0 + sl1;
n = sl0;
L50:;
sl0 = fasloc1;
sl1 = 1;
sl0 = sl0 + sl1;
fasloc1 = sl0;
L58:;
goto L4;
L60:;
sl0 = fasloc1;
return sl0;
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
long loc2;
long loc4;
long loc5;
long loc7;
long loc8;
sl0 = 1;
loc2 = sl0;
sl0 = 0;
loc4 = sl0;
sl0 = 1000000;
loc5 = sl0;
sl1 = 1;
sl2 = loc5;
L64:;
long for0 = sl1;
long for1 = sl2;
for (long for3 = for0; for3 < for1; for3 += 1) {
sl1 = for3;
loc7 = sl1;
sl2 = loc7;
sl1 = c(sl2);
loc8 = sl1;
sl1 = loc8;
sl2 = loc4;
sl1 = sl1 > sl2;
if(!sl1){
goto L100;
}
sl1 = loc8;
loc4 = sl1;
sl1 = loc7;
loc2 = sl1;
L100:;
}
L102:;
sl2 = loc2;
printf("%ld\n", sl2);
return 0;
}
