// 题目描述
// 有一只快乐的蠕虫居住在一个m×n大小的网格中。在网格的某些位置放置了k块石头。网格中的每个位置要么是空的，要么放置了一块石头。当蠕虫睡觉时，它在水平方向或垂直方向上躺着，把身体尽可能伸展开来。蠕虫的身躯既不能进入到放有石块的方格中，也不能伸出网格外。而且蠕虫的长度不会短于2个方格的大小。
// 本题的任务是给定网格，要计算蠕虫可以在多少个不同的位置躺下睡觉。
// 输入
// 输入文件的第1行是一个整数t，1<=t<=11,表示测试数据的个数。每个测试数据的第1行为3个整数：m,n和k(0<=m,n,k<=200000),接下来有k行，每行为2个整数，描述了一块石头的位置（行和列，最左上角位置为（1,1））。
// 输出
// 对每个测试数据，输出占一行，为一个整数，表示蠕虫可以躺着睡觉的不同位置的数目。
#include<stdio.h>
int main()
{
    int t;
    scanf("%d",&t);
    while(t--)
    {
        int m,n,k;
        scanf("%d %d %d",&m,&n,&k);
        int stone[m+1][n+1];
        for(int i=1;i<=m;i++)
            for(int j=1;j<=n;j++)
                stone[i][j]=0;
        for(int i=0;i<k;i++)
        {
            int x,y;
            scanf("%d %d",&x,&y);
            stone[x][y]=1;
        }
        int count=0;
        // 计算水平位置
        for(int i=1;i<=m;i++)
        {
            int len=0;
            for(int j=1;j<=n;j++)
            {
                if(stone[i][j]==0)
                    len++;
                else
                {
                    if(len>=2)
                        count++;
                    len=0;
                }
            }
            if(len>=2)
                count++;
        }
        // 计算垂直位置
        for(int j=1;j<=n;j++)
        {
            int len=0;
            for(int i=1;i<=m;i++)
            {
                if(stone[i][j]==0)
                    len++;
                else
                {
                    if(len>=2)
                        count++;
                    len=0;
                }
            }
            if(len>=2)
                count++;
        }
        printf("%d\n",count);
    }
    return 0;
}