#include <stdio.h>

int main() {
    char buf[64];
    printf("%p\n", buf);
    fflush(stdout);
    scanf("%s", buf);
    printf("Got: %s\n", buf);
}
