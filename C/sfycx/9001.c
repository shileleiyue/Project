// 题目描述
// 孩子们是这样学习多位数的加法：将两个加数右对齐，然后从右到左每次加一位。这种情况下经常会产生进位，即两位相加结果若大于等于10就向左进一位。对于孩子们来说，判断进位具有一定的挑战性。你的任务是：给定任意的两个加数，要求统计出进位的次数，以帮助教育者评估该加法的难度。
// 输入
// 每一行是两个少于10位的无符号整数，最后一行为0 0，表示输入结束。
// 输出
// 对输入文件的每一行（除最后一行外），计算它们在相加时进位的次数并输出。按照输出样例的格式输出。
// 样例输入 复制
// 123 456
// 555 555
// 123 594
// 0 0
// 样例输出 复制
// No carry operation.
// 3 carry operations.
// 1 carry operation.

#include<stdio.h>
#include<string.h>

void stdint(const char* a,int* b){
    int l=strlen(a);
    for (int i = 0; i < l; i++)
    {
        b[i]=a[l-i-1]-'0';
    }
}

int main(){
    
    char a2[10],b2[10];
    while(scanf("%s %s",a2,b2)!=EOF)
    {
        int a1[10]={0},b1[10]={0},c1[20]={0},t=0;
        if(a2[0]=='0')break;
        stdint(a2,a1);
        stdint(b2,b1);
        for(int i=0;i<10;i++){
            c1[2*i]=a1[i]+b1[i];
            if(i>0)c1[2*i]+=c1[2*i-1];
            if(c1[2*i]>9){
                c1[2*i+1]=c1[2*i]/9;
                c1[2*i]=c1[2*i]%10;
                if(c1[2*i+1]!=0)t++;
            }
        }
        if(t==0){
            printf("No carry operation.\n");
        }
        else if(t==1){
            printf("%d carry operation.\n",t);
        }
        else{
            printf("%d carry operations.\n",t);
        }
    }
    return 0;
}