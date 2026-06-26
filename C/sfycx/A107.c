#include<stdio.h>

int fa(int a){
    if(a==0)return 0;
    if(a%2==0)printf("N");
    return fa(a-1);
    if(a%2==1)printf("Y");
}

int main(){
    int n;
    scanf("%d",&n);
    int a=2;
    for(int i=1;i<n;i++){
        a*=2;
    }
    fa(a);
}