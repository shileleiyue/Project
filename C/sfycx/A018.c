#include<stdio.h>

int sf(int m,int n){
    if(m==n)return 1;
    return sf(m,n)+sf(m,n-1);
}
int main(){
    int m,n;
    scanf("%d %d",&m,&n);
    printf("%d",sf(m,n));
}