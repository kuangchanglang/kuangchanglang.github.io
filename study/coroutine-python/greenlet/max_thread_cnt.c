#include<stdio.h>
#include <pthread.h>
#include <unistd.h>
#define MAX 40000

void *sleep1k(void){
    sleep(1000);
    return NULL;
}

int main()
{
    int i = 0;
    pthread_t thread;

    while (1) {
        if (pthread_create(&thread, NULL,(void *)sleep1k, NULL) != 0){
            break;
        }
        i ++;
        if(i >=MAX) {
            break;
        }
    }
    printf("i = %d\n", i);
    getchar();
    return 0;
}
