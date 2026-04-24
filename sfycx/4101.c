#include <stdio.h>
#include <string.h>
int main()
{
    int n, l, t, max, i, j, num[26];
    char str[1001];

    scanf("%d", &n);
    for (i = 0; i < n; i++)
    {
        memset(num, 0, sizeof(num));
        scanf("%s", str);
        l = strlen(str);
        for (j = 0; j < l; j++)
        {
            t = str[j] - 'a';
            num[t]++;
        }
        max = 0;
        for (j = 25; j >= 0; j--)
        {
            if (num[j] >= num[max])
                max = j;
        }
        printf("%c %d\n", max + 'a', num[max]);
    }

    return 0;
}