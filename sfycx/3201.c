// 题目描述
// 读入两个小于10000的正整数A和B，计算A+B。需要注意的是：如果A和B的末尾K（不超过8）位数字相同，请直接输出-1。
// 输入
// 测试输入包含若干测试数据，每个测试数据占一行，格式为A B K，相邻两数字有一个空格间隔。当A和B同时为0时输入结束，相应的结果不要输出。
// 输出
// 对每个测试数据输出1行，即A+B的值或者是-1。
#include<stdio.h>
#include<math.h>
int main(){
    int a,b,k;
    for (scanf("%d %d %d",&a,&b,&k);a!=0||b!=0;scanf("%d %d %d",&a,&b,&k)){
        int pow10k=pow(10,k);
        if(a%pow10k==b%pow10k){
            printf("-1\n");
        }
        else{
            printf("%d\n", a + b);
        }
    }
    return 0;
}