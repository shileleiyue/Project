// 题目描述
// 此题为插入排序
// 此题用作练习题，请用插入排序完成此题。
// 输入
// 第一行输入一个整数n（0<n<=100000)，表示有n个待排序数据;
// 随后的n行每行输入一个整数。
// 输出
// 升序输出排序结果

#include<stdio.h>
int main(){
    long long n;
    scanf("%lld",&n);
    int Sort[n+1];
    for(long long i=0;i<n;i++){
        scanf("%d",&Sort[i]);
    }
    for(long long i=0;i<n;i++){
        for(long long j=i;j<n;j++){
            if(Sort[j]<Sort[i]){
                int temp;
                temp=Sort[j];
                Sort[j]=Sort[i];
                Sort[i]=temp;
            }
        }
    }
    for(long long i=0;i<n;i++){
        printf("%d ",Sort[i]);
    }
    return 0;
}