#include<stdio.h>

int YingShu(int a){
    int x=1;
    if(a<=2)return x;
    for(int i=1;i<=a/2;i++){
        if(a%i==0&&a/i>0){
            a/=i;
            return YingShu(a);
            x++;
        }
    }
    return x;

}

int main(){
    int n;
    scanf("%d",&n);
    while(n--){
        int a;
        scanf("%d",&a);
        printf("%d\n",YingShu(a));
    }
}