#include<stdio.h>
int main()
{
    //freopen("1002in.txt","r",stdin);
    //freopen("1002out.txt","w",stdout);
    int a,b;
    while(scanf("%d %d",&a,&b)!=EOF)
        printf("%d\n",a+b);
    return 0;
}