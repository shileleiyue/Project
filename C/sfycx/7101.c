// 题目描述
// 一个名叫是PigHeadThree的研究组织设计了一台实验用的计算机，命名为PpMm。PpMm只能执行简单的六种命令A，B，C，D，E，F；只有二个内存M1，M2；三个寄存器R1，R2，R3。六种命令的含义如下：
// 命令A：将内存M1的数据装到寄存器R1中；
// 命令B：将内存M2的数据装到寄存器R2中；
// 命令C：将寄存器R3的数据装到内存M1中；
// 命令D：将寄存器R3的数据装到内存M2中；
// 命令E：将寄存器R1中的数据和寄存器R2中的数据相加，结果放到寄存器R3中；
// 命令F：将寄存器R1中的数据和寄存器R2中的数据相减，结果放到寄存器R3中。
// 你的任务是：设计一个程序模拟PpMm的运行。
// 输入
// 有若干组，每组有2行，第一行是2个整数，分别表示M1和M2中的初始内容；第二行是一串长度不超过200的由大写字母A到F组成的命令串，命令串的含义如上所述。
// 输出
// 对应每一组的输入，输出只有一行，二个整数，分别表示M1，M2的内容；其中M1和M2之间用逗号隔开。
// 其他说明：R1，R2，R3的初始值为0，所有中间结果都在-231和231之间。
// 样例输入 复制
// 100 288
// ABECED
// 876356 321456
// ABECAEDBECAF
// 样例输出 复制
// 388,388
// 2717080,1519268


#include<stdio.h>
#include<string.h>

int main(){
    long m1,m2,r1=0,r2=0,r3=0;
    while (scanf("%ld %ld",&m1,&m2)!=EOF)
    {
        char fct[201];
        scanf("%s",fct);
        int l=strlen(fct);
        for(int i=0;i<l;i++)
        {
            switch(fct[i]){
                case 'A':{
                    r1=m1;
                }break;
                case 'B':{
                    r2=m2;
                }break;
                case 'C':{
                    m1=r3;
                }break;
                case 'D':{
                    m2=r3;
                }break;
                case 'E':{
                    r3=r1+r2;
                }break;
                case 'F':{
                    r3=r1-r2;
                }break;
            }
        }
        printf("%ld,%ld\n",m1,m2);
    }
    return 0;
}