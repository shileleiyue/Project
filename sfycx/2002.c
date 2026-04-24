#include<stdio.h>
int main(){
    int a,b;
    char c;
    for (scanf("%d %d %c",&a,&b,&c);a!=0&&b!=0;scanf("%d %d %c",&a,&b,&c))
    {
        switch (c)
        {
        case '+':printf("%d %c %d = %d\n",a,c,b,a+b);break;
        case '-':printf("%d %c %d = %d\n",a,c,b,a-b);break;
        case '*':printf("%d %c %d = %d\n",a,c,b,a*b);break;
        case '%':printf("%d %c %d = %d\n",a,c,b,a%b);break;
        case '/':
            if(a%b==0)printf("%d %c %d = %d\n",a,c,b,a/b);
            else printf("%d %c %d = %.2f\n",a,c,b,1.0*a/b);
        }
    }
    
}