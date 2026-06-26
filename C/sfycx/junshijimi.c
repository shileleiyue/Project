// 题目描述
// 我军方截获的信息由n（n<=30000）个数字组成，因为是敌国的高端秘密，所以一时不能破获。最原始的想法就是对这n个数进行从小到大排序，每个数都对应一个序号，然后对第i个是什么感兴趣，现在要求编程完成。
// 输入
// 第一行是n,第二行是n个截获的数字，第三行是数字k，接着是k行要输出数的序号。
// 输出
// k行序号所对应的数字。

#include<stdio.h>
#include<stdlib.h>
int cmp_int_asc(const void *a, const void *b) {
    int x = *(const int *)a;
    int y = *(const int *)b;

    if (x < y) return -1;
    if (x > y) return 1;
    return 0;
}

int main(){
    int n,k;
    scanf("%d",&n);
    int Num[n+1];
    for (int i = 0; i < n; i++)
    {
        scanf("%d",&Num[i]);
    }
    qsort(Num, n, sizeof(Num[0]), cmp_int_asc);
    scanf("%d",&k);
    int x;
    while(k--)
    {
        scanf("%d",&x);
        printf("%d\n",Num[x-1]);
    }
    
    return 0;
}