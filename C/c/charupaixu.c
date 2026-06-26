#include<stdio.h>
#include<string.h>
int main()
{
    char a[10][10]={"John","Lewis","Nathan","Pat","Quincy","Roger","Stan","Tom","Alice","Bob"};
    int i,j,t;
    char q[10];

    for(j=0;j<10;j++) 
        for(i=j;i<10;i++)
            if(strcmp(*a[i],*a[t])<0)t=i;
            if(strcmp(*a[i],*a[i+1])>0)
            {
                strcpy(q[10],a[0]);strcpy(a[i],a[i+1]);strcpy(a[i],q[10]);
            }
            
    for(i=0;i<10;i++)
    {
        printf("%s",a[i]);
        printf(" ");
    }
    return 0;
}