#include<stdio.h>

int ZuHeShu(int m,int n){
    if(n==1)return m;
    if(m<0||n<0||m<n)return 0;
    if(m==n)return 1;
    return ZuHeShu(m-1,n)+ZuHeShu(m-1,n-1);
}

int main(){
    int n;
    scanf("%d",&n);
    while(n--){
        int m,n;
        scanf("%d %d",&m,&n);
        printf("%d\n",ZuHeShu(m,n));
    }
}