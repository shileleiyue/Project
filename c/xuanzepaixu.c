#include<stdio.h>
#include<string.h>
int main()
{
    char a[10][10]={"John","Lewis","Nathan","Pat","Quincy","Roger","Stan","Tom","Alice","Bob"};
    int i,j,t;
    char q[10];
    for(j=0;j<10;j++)
    {
        t=j;
        for(i=j;i<10;i++)
            if(strcmp(a[i],a[t])<0)t=i;
        strcpy(q,a[t]);strcpy(a[t],a[j]);strcpy(a[j],q);
    }
    for(i=0;i<10;i++)
    {
        printf("%s",a[i]);
        printf(" ");
    }
    return 0;
}