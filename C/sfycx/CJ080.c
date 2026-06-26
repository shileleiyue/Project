#include<stdio.h>
int main(){
    int sum=0;
    char str[101];
    while(scanf("%s",str)!=EOF){
        sum++;
    }
    printf("%d\n",sum);

    return 0;
}