#include<stdio.h>
int main()
{
    //freopen("1004in.txt","r",stdin);
    //freopen("1004out.txt","w",stdout);
    int i,t,sum,n;
    for (scanf("%d",&n); n!=0;scanf("%d",&n))
    {
        sum=0;
        for ( i = 0;i<n; i++)
        {
            scanf("%d",&t);
            sum+=t;
        }
        printf("%d\n",sum);
    }
    return 0;
}