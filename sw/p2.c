#include <stdio.h>
#include <string.h>


#define BUF_SIZE 100002

int ctoi(char c)
{
    return (int)c - (int)'0';
}

char itoc(int i)
{
    return (char)(i + (int)'0');
}


int main()
{
    setbuf(stdout, NULL);
    char N[BUF_SIZE], M[BUF_SIZE];
    int T, x, y;

    scanf("%d", &T);
    for (int t = 0; t < T; t++)
    {
        x = 0;
        y = 0;
        for (int i = 0; i < BUF_SIZE; i++)
        {
            N[i] = '\0';
            M[i] = '\0';
        }
        
        scanf("%s %d %d", N, &x, &y);
        int n, j = 0, fail = 0, fill = 0;
        while (!fail && (N[j] != '\0'))
        {
            n = ctoi(N[j]);
            
            if (fill || n >= y) M[j] = itoc(y);
            else if (n >= x)    M[j] = itoc(x);
            else fail = 1;

            if (n > ctoi(M[j])) fill = 1;
            j++;
        }
        printf("#%d ", t + 1);

        if (fail) {
            int len = strlen(&N[0]);
            if (len <= 1)
            {
                printf("-1");
            }
            else
            {
                j = 0;
                for (j = 0; j < len - 1; j++)
                {
                    M[j] = itoc(y);
                }
                M[j] = '\0';
                printf("%s", M);
            }
        } else {
            if (M[0] == '0')
                printf("-1");
            else
                printf("%s", M);
        }
        printf("\n");
    }

    return 0;
}