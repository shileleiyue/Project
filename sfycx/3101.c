// 题目描述
// 班上有学生若干名，给出每名学生的年龄（整数），求班上所有学生的平均年龄，按要求输出结果。
// 输入
// 第一行有一个整数n（1 <= n <= 100），表示学生的人数。其后n行每行有1个整数，取值为15到25。
// 输出
// 输出一行，为要求的平均年龄，如果为整数，则直接输出该整数，如果为小数，则保留到小数点后1位。
#include <stdio.h>
int main(){
    int n;
    scanf("%d",&n);
    int sum=0;
    for(int i=0;i<n;i++){
        int age;
        scanf("%d",&age);
        sum+=age;
    }
    double avg=(double)sum/n;
    if(avg==(int)avg){
        printf("%d\n",(int)avg);
    }else{
        printf("%.1lf\n",avg);
    }
    return 0;
}