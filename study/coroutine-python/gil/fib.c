#include<stdio.h>

int num = 30;

int fib(int n){
    if(n <= 0){
        return 0;
    }
    if(n < 2){
        return 1;
    }
    return fib(n-1) + fib(n-2);
}

int main(){
    printf("%d\n", fib(num));
}
