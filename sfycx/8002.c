// 题目描述
// 给定一个数字序列{X1, X2, ... , Xn}, 假定 Xk = (A * k + B) % mod。你的任务就是找一个最大的子序列{Y1, Y2, ... , Ym} ，对于每对 (Yi, Yj)要求满足Yi + Yj <= L (1 ≤ i < j ≤ m), 而且同时满足Yi <= L (1 ≤ i ≤ m )。
// 现在给定n，L，A，B和mod，你的任务就是找出上述最大的m值。
// 输入
// 输入包括多组测试数据，直到文件尾。每个测试数据占一行，包括5个整数： n, L, A, B 和mod. (1 ≤ n ≤ 2 * 107, 1 ≤ L ≤ 2 * 109, 1 ≤ A, B, mod ≤ 109)
// 输出
// 对于每组测试数据，输出m值，占一行。
// 样例输入 复制
// 1 8 2 3 6
// 5 8 2 3 6
// 样例输出 复制
// 1
// 4

#include<stdio.h>
int main(){
    int n,l,a,b,,mod;
    while(scanf("%d %d %d %d %d",&n,l,&a,&b,&mod)!=EOF){
        int ll=l/2,min=l,max=0,m;
        for(int i=1;i<=n;i++){
            xk=(a*k+b)%mod;
            if(xk<ll){
                m++;
                max=xk;
            }

        }

    }
    return 0;
}