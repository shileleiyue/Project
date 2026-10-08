// 题目描述
// 给出m个字符串，要求输出重复n次的字符串有几个。
// 输入
// 先给定一个N，N≤100000，接着输入N个字符串。
// 输出
// 对于每组测试数据，输出若干行，每行两个正整数，第一个数表示重复的次数，第二个数表示在此重复次数下有几种不同的字符串。
// 样例输入 复制
// 5
// BBA
// BBA
// BEA
// DEC
// CCF
// 样例输出 复制
// 1 3
// 2 1
#include<stdio.h>
#include<string.h>
int main(){
    int n;
    scanf("%d",&n);
    char str[100][101];
    int count[100]={0};
    for(int i=0;i<n;i++){
        scanf("%s",str[i]);
        count[i]=1;
        for(int j=0;j<i;j++){
            if(strcmp(str[i],str[j])==0){
                count[j]++;
                count[i]=0;
                break;
            }
        }
    }
    int freq[100]={0};
    for(int i=0;i<n;i++){
        if(count[i]>0){
            freq[count[i]]++;
        }
    }
    for(int i=1;i<=n;i++){
        if(freq[i]>0){
            printf("%d %d\n",i,freq[i]);
        }
    }
    return 0;
}