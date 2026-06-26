#include<stdio.h>
#include<string.h>
int main()
{
    char a[][10]={"John","Lewis","Nathan","Pat","Quincy","Roger","Stan","Tom","Alice","Bob"};
    int i,j;
    char q[10];
    for(j=0;j<10;j++)
        for(i=0;i<10-j-1;i++)
            if(strcmp(a[i],a[i+1])>0)
            {
                strcpy(q,a[i]);
                strcpy(a[i],a[i+1]);
                strcpy(a[i+1],q);
            }
    for(i=0;i<10;i++)
    {
        printf("%s ",a[i]);
    }
    return 0;
}