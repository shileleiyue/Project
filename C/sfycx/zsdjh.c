// 题目描述
// 现在给你一个由n个互不相同的整数组成的序列，现在要求你任意交换相邻的两个数字，使序列成为升序序列，请问最少的交换次数是多少？
// 输入
// 输入包含多组测试数据。每组输入第一行是一个正整数n（n<500000），表示序列的长度，当n=0时结束。
// 接下来的n行，每行一个整数a[i]（0<=a[i]<=999999999），表示序列中第i个元素。
// 输出
// 对于每组输入，快速输出使得所给序列升序的最少交换次数。
#include<stdio.h>
int main(){
    int n;
    while(scanf("%d",&n)!=EOF&&n!=0){
        int a[n+1];
        for(int i=0;i<n;i++){
            scanf("%d",&a[i]);
        }
        long long sum=0;
        for(int i=0;i<n-1;i++){
            for(int j=i;j<n;j++){
                if(a[j]<a[i]){
                    int temp;
                    temp=a[j];
                    a[j]=a[i];
                    a[i]=temp;
                    sum++;
                }
            }
        }
        printf("%lld\n",sum);
    }
    return 0;
}