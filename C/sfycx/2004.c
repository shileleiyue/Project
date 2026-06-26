// 输入
// 第1 行是测试数据的组数n，后面跟着n行输入。每组测试数据占1行，包括一个正整数a (a < 32768) 。

// 输出
// n 行，每行输出对应一个输入。输出是两个正整数，第一个是最少的动物数，第二个是最多的动物数，两个正整数用空格分开。如果没有满足要求的情况出现，则输出2个0。
#include<stdio.h>
#include<math.h>
int main(){
    int n;
    scanf("%d",&n);
    while(n--){
        int a;
        scanf("%d",&a);
        int min=0,max=0;
        for(int i=0;i<=a/4;i++){
            for(int j=0;j<=a/2;j++){
                if(4*i+2*j==a){
                    if(i+j<min||min==0){
                        min=i+j;
                    }
                    if(i+j>max){
                        max=i+j;
                    }
                }
            }
        }
        if(min!=0&&max!=0){
            printf("%d %d\n",min,max);
        }else{
            printf("0 0\n");
        }
    }
    return 0;
}