#include <stdio.h>
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
long loc0;
long loc3;
long loc5;
sl0 = 0;
loc0 = sl0;
sl0 = 10000000;
loc3 = sl0;
sl1 = loc3;
L34:;
long for1 = sl1;
for (long for3 = 0; for3 < for1; for3 += 1) {
sl1 = for3;
loc5 = sl1;
sl1 = loc0;
sl2 = loc5;
sl1 = sl1 + sl2;
loc0 = sl1;
L46:;
}
L48:;
sl2 = loc3;
sl3 = loc0;
printf("%ld %ld\n", sl2, sl3);
return 0;
}
