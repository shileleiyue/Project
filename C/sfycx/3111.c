// 输入
// 输入包含多组测试数据，每组只有一行，包括两个不大于1000的正整数。
// 输出
// 对于每个测试数据，给出这两个数的最小公倍数，每个实例输出一行
#include<stdio.h>
#include<math.h>
int gcd(int a,int b){
    return b==0?a:gcd(b,a%b);
}
int main(){
    int a,b;
    while(scanf("%d %d",&a,&b)!=EOF){
        if(a==0&&b==0){
            break;
        }
        int lcm=a/gcd(a,b)*b;
        printf("%d\n",lcm);
    }
    return 0;
}