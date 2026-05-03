#include <stdio.h>
int main()
{
    int n;
    for (scanf("%d", &n); n != 0; scanf("%d", &n))
    {
        int a, sum = 0;
        for (int i = 0; i < n; i++)
        {
            scanf("%d", &a);
            sum += a;
        }
        printf("%d\n", sum);
    }
    return 0;
}