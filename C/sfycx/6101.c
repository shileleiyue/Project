#include <stdio.h> //判断某年是否是闰年。
int main(){
    int year;
    while(scanf("%d",&year)!=EOF){
        if((year%4==0 && year%100!=0) || year%400==0){
            printf("Y\n");
        }else{
            printf("N\n");
        }
    }
    return 0;
}