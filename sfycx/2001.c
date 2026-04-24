#include<stdio.h>
int main()
{
    int i,j,n,p;
    long  a,b,c,fn;
    scanf("%d",&p);
    for(i=1;i<=p;i++)
    {
        b=0;c=1;
        scanf("%d,%ld",&n,&a);
        for(j=1;j<=n;j++){
            fn=b+c;
            b=c;c=fn;
        }
        if (a<=fn)printf("Yes");
        else printf("No");
    }
    return 0;
}
