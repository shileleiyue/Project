#include<stdio.h>
int main() {
    float sum,num;
    for(int i=0;i<12;i++){
        scanf("%f",&num);
        if(num>0){
            sum+=num;
        }
    }
    printf("$%.2f\n",sum/12);
    return 0;
}
