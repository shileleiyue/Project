// 题目描述
// 本次大赛正式开始了。看着各色各样的气球飘扬在赛场上是多么令人兴奋。作为HDU最好的程序员之一的你，只要你能解决一个非常简单的简单的不能再简单的题目，你就会得到一个漂亮的气球。给你一个运算符（+、-、* 、/，表示加、减、乘、除）和两个正整数，你的任务就是求出它们的运算结果，简单吧，来吧。只要完成任务，漂亮妹妹会马上送给你一个美丽的气球。祝你好运！
// 输入
// 输入包含多组测试样例，第一行有一个整数T（0 < T < 1000），表示测试样例的组数。然后是T组测试样例，每组包含一个字符C（+、-、* 、/）和两个正整数A和B（0 < A,B < 10000）。当然，A和B是操作数，C是运算符。
// 输出
// 对于每组测试输出样例其运算结果，当且仅当结果不是整数时，保留2位小数。
#include <stdio.h>
int main(){
    int T;
    scanf("%d",&T);
    while(T--){
        char C;
        int A,B;
        scanf(" %c %d %d",&C,&A,&B);
        double result;
        switch (C)
        {
        case '+':
            result=A+B;
            break;
        case '-':
            result=A-B;
            break;
        case '*':
            result=A*B;
            break;
        case '/':
            result=(double)A/B;
            break;
        }
        if(result==(int)result){
            printf("%d\n",(int)result);
        }else{
            printf("%.2lf\n",result);
        }
    }
    return 0;
}