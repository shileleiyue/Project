// 题目描述
// 判断两个由大小写字母和空格组成的字符串在忽略大小写和压缩掉空格后是否相等。
// 输入
// 第1行是测试数据的组数n，每组测试数据占2行，第1行是第一个字符串s1，第2行是第二个字符串s2。
// 每组测试数据之间有一个空行，每行数据不超过100个字符（注意字符串的长度可能为0）。
// 输出
// n行，相等则输出YES，否则输出NO。
#include<stdio.h>
int main(){
    int n,i,j;
    char s1[101],s2[101];
    scanf("%d",&n);
    getchar();
    for(i=0;i<n;i++){
        gets(s1);
        gets(s2);
        for(j=0;s1[j];j++){
            if(s1[j]>='A'&&s1[j]<='Z')
                s1[j]=s1[j]-'A'+'a';
            else if(s1[j]==' ')
                s1[j]=0;
        }
        for(j=0;s2[j];j++){
            if(s2[j]>='A'&&s2[j]<='Z')
                s2[j]=s2[j]-'A'+'a';
            else if(s2[j]==' ')
                s2[j]=0;
        }
        if(strcmp(s1,s2)==0)
            printf("YES\n");
        else
            printf("NO\n");
    }
    return 0;
}