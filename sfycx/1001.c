#include<stdio.h>
int main(){
    int n,a,b,i;//-2^31~2^31-1 整型%d
    //long  -2^63~2?^63-1  长整型%ld
    //float 浮点型%f
    //double 双精度%lf
    //char 字符%s(字符串)/%c（字母1）
    scanf("%d",&n);
    for(i=0;i<n;i++){
        scanf("%d %d",&a,&b);
        printf("%d\n",a+b);
    }
}