// 题目描述
// 冒泡排序（Bubble Sort），是一种计算机领域的较简单的排序算法。 它重复地走访过要排序的数列，一次比较两个元素，如果他们的顺序错误就把他们交换过来。走访数列的工作是重复地进行直到没有再需要交换，也就是说该数列已经排序完成。 这个算法的名字由来是因为越小的元素会经由交换慢慢“浮”到数列的顶端，故名。
// 由于冒泡排序简洁的特点，它通常被用来对于计算机程序设计入门的学生介绍算法的概念。

// 此题用作练习题，请用冒泡排序完成此题。

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
    for(long long i=n-1;i>=0;i--){
        int temp;
        for(long long j=0;j<i;j++){
            if(Sort[j]>Sort[j+1]){
                temp=Sort[j];
                Sort[j]=Sort[j+1];
                Sort[j+1]=temp;
            }
        }
    }
    for(long long i=0;i<n;i++){
        printf("%d ",Sort[i]);
    }
    return 0;
}