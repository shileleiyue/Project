#include <stdio.h>
#include <string.h>
int main()
{
    int n, m, i, j;
    char strid[2][16], strin[9], strout[9], tstrid[16], tstrin[9], tstrout[9];
    scanf("%d", &n);
    for (i = 0; i < n; i++)
    {
        scanf("%d", &m);
        strcpy(strin, "23:59:59");
        strcpy(strout, "00:00:00");
        scanf("%s %s %s", strid[0], strin, strout);
        strcpy(strid[1],strid[0]);
        for (j = 1; j < m; j++)
        {
            scanf("%s %s %s", tstrid, tstrin, tstrout);
            if (strcmp(tstrin, strin) < 0)
            {
                strcpy(strin, tstrin);
                strcpy(strid[0], tstrid);
            }
            if (strcmp(tstrout, strout) > 0)
            {
                strcpy(strout, tstrout);
                strcpy(strid[1], tstrid);
            }
        }
        printf("%s %s\n", strid[0], strid[1]);
    }

    return 0;
}