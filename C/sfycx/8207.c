// 题目描述
// 本题的任务是对小于1,000,000的整数验证哥德巴赫猜想。
// 输入
// 输入文件包含一个或多个测试数据，每个测试数据为一个整数n，6 <= n < 1000000。n=0表示输入结束。
// 输出
// 对每个测试数据n，输出一行，格式为：n=a+b，其中a和b均为素数。数和运算符之间用一个空格隔开。如果存在多对素数满足要求，则选择差值（b-a）最大的那对。如果不存在这样的素数对，则输出“Goldbach's conjecture is wrong.”。
// 样例输入 复制
// 8
// 20
// 42
// 0
// 样例输出 复制
// 8 = 3 + 5
// 20 = 3 + 17
// 42 = 5 + 37

#include<stdio.h>

int sushu(int x){
    for(int j=2;j<x;j++){
        if(x%j==0){
            return 0;
        }
    }
    return 1;
}

int main(){
    int n;
    for(scanf("%d",&n);n!=0;scanf("%d",&n)){
        int t=0;
        for(int i=2;i<n/2;i++){
            int j=n-i;
            if(n%2==1){
                printf("Goldbach's conjecture is wrong.\n");
                t=1;
                break;
            }
            else if(sushu(i)+sushu(j)==2){
                printf("%d = %d + %d\n",n,i,j);
                t=1;
                break;
            }
        }
        if(t==0)printf("Goldbach's conjecture is wrong.\n");
    }
    return 0;
}