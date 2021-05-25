#include <stdio.h>
long p(long n) {long sl0;
long sl1;
double sd0;
double sd1;
char* sc0;
char* sc1;
long fasloc1;
sl0 = n;
sl1 = 4;
sl0 = sl0 < sl1;
if(!sl0){
goto L16;
}
sl0 = n;
sl1 = 1;
sl0 = sl0 > sl1;
return sl0;
L16:;
sl0 = n;
sl1 = 2;
sl0 = sl0 % sl1;
if(!sl0){
goto L32;
}
sl0 = n;
sl1 = 3;
sl0 = sl0 % sl1;
if(sl0){
goto L36;
}
L32:;
sl0 = 0;
return sl0;
L36:;
sl0 = 5;
fasloc1 = sl0;
L40:;
sl0 = fasloc1;
sl1 = fasloc1;
sl0 = sl0 * sl1;
sl1 = n;
sl0 = sl0 <= sl1;
if(!sl0){
goto L94;
}
sl0 = n;
sl1 = fasloc1;
sl0 = sl0 % sl1;
if(sl0){
goto L64;
}
sl0 = 0;
return sl0;
L64:;
sl0 = fasloc1;
sl1 = 2;
sl0 = sl0 + sl1;
fasloc1 = sl0;
sl0 = n;
sl1 = fasloc1;
sl0 = sl0 % sl1;
if(sl0){
goto L84;
}
sl0 = 0;
return sl0;
L84:;
sl0 = fasloc1;
sl1 = 4;
sl0 = sl0 + sl1;
fasloc1 = sl0;
L92:;
goto L40;
L94:;
sl0 = 1;
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
long loc3;
long loc6;
sl0 = 0;
loc3 = sl0;
sl1 = 1000000;
L38:;
long for1 = sl1;
for (long for3 = 0; for3 < for1; for3 += 1) {
sl1 = for3;
loc6 = sl1;
sl1 = loc3;
sl3 = loc6;
sl2 = p(sl3);
sl1 = sl1 + sl2;
loc3 = sl1;
L54:;
}
L56:;
sl2 = loc3;
printf("%ld\n", sl2);
return 0;
}
