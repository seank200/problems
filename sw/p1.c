#include <stdio.h>
#include <stdlib.h>

int max_num_bought;
int num_bought;
int bought[26];
char** gifts;
int** visited;
int R, C;


void dfs(int r, int c)
{
    visited[r][c] = 1;
    bought[(int)gifts[r][c] - (int)'A'] = 1;
    num_bought++;

    int r_dir[4] = { 0, 0, 1, -1 }; // EWSN
    int c_dir[4] = { 1, -1, 0, 0 }; // EWSN

    int nr, nc;
    int moved = 0;
    for (int d = 0; d < 4; d++)
    {
        nr = r + r_dir[d];
        nc = c + c_dir[d];
        if (0 <= nr && nr < R && 0 <= nc && nc < C)
        {
            if (!visited[nr][nc])
            {
                if (!bought[(int)gifts[nr][nc] - (int)'A'])
                {
                    moved = 1;
                    dfs(nr, nc);
                    visited[nr][nc] = 0;
                }
            }
        }
    }

    if (!moved)
        if (num_bought > max_num_bought)
            max_num_bought = num_bought;

    bought[(int)gifts[r][c] - (int)'A'] = 0;
    num_bought--;
}


int main()
{
    setbuf(stdout, NULL);   
    int T;
    scanf("%d", &T);

    int* answers = (int*)malloc(sizeof(int) * T);

    for (int t = 0; t < T; t++)
    {
        scanf("%d %d", &R, &C);

        max_num_bought = 0;
        num_bought = 0;
        for (int i = 0; i < 26; i++)
            bought[i] = 0;

        gifts = (char**)malloc(sizeof(char*) * R);
        visited = (int**)malloc(sizeof(int*) * R);
        for (int r = 0; r < R; r++)
        {
            gifts[r] = (char*)malloc(sizeof(char) * C);
            visited[r] = (int*)malloc(sizeof(int) * C);
            for (int c = 0; c < C; c++)
                visited[r][c] = 0;
        }

        char gift;
        for (int r = 0; r < R; r++)
        {
            for (int c = 0; c < C; c++)
            {
                scanf("%c", &gift);
                while(gift == '\n')
                    scanf("%c", &gift);
                gifts[r][c] = gift;
            }
        }

        dfs(0, 0);
        answers[t] = max_num_bought;

        for (int r = 0; r < R; r++)
        {
            free(gifts[r]);
            free(visited[r]);
        }
        free(gifts);
        free(visited);
    }

    for (int t = 0; t < T; t++)
        printf("#%d %d\n", t + 1, answers[t]);

    return 0;
}