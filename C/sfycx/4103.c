#include<stdio.h>
#include<string.h>
int main()
{
    int p,q;
    char s[100000],t[100000];
    while(scanf("%s %s",s,t)!=EOF)
    {
        p=strlen(s);
        q=strlen(t);
        int j=0;
        for (int i = 0; i < p;)
        {
            for (; j < q; j++)
            {           
                if (s[i] == t[j])
                {
                    i++;
                }
            }
            if (i==p)
            {
                printf("Yes\n");
                break;
            }
            if (j==q||i<p)
            {
                printf("No\n");
                break;
            }
            
        }
        
    }
    return 0;
}