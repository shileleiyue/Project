// 输入
// 输入一系列的温度，每个温度占一行，温度的范围从-10 到200，温度精确到小数点后两位。数字999表示输入数据结束。数据集中至少有两个温度。
// 输出
// 你的程序将输出一系列温度的差值。差值需要保留小数点两位，并且没有前导0（除非小于1，例如0.01）或空格。
// 所有输出结束后，输出一行End of Output。
#include<stdio.h>
int main(){
    double temp[100],diff;
    int i=0;
    while(scanf("%lf",&temp[i])!=EOF){
        if(temp[i]==999){
            break;
        }
        i++;
    }
    for(int j=0;j<i-1;j++){
        diff=temp[j+1]-temp[j];
        printf("%.2lf\n",diff);
    }
    printf("End of Output\n");
    return 0;
}