#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

// grid_len은 배열 grid의 길이입니다.
// 파라미터로 주어지는 문자열은 const로 주어집니다. 변경하려면 문자열을 복사해서 사용하세요.

// 0: Right, 1: Up, 2: Left, 3: Down
int move[4][2] = {{1, 0}, {0, -1}, {-1, 0}, {0, 1}};
int turn(char direction)
{
    if (direction == 'L')
        return 1;
    if (direction == 'R')
        return -1;
    if (direction == 'S')
        return 0;
}

int cmpfunc(const void *a, const void *b)
{
    return (*(int *)a - *(int *)b);
}

int *solution(const char *grid[], size_t grid_len)
{
    int cycle_lengths_size = 16;
    int cycle_lengths_cnt = 0;
    int *cycle_lengths = (int *)malloc(sizeof(int) * cycle_lengths_size);

    size_t gy = grid_len;
    size_t gx = strlen(grid[0]);

    // init visited
    int ***visited = (int ***)malloc(sizeof(int **) * gy);
    for (int y = 0; y < gy; y++)
    {
        visited[y] = (int **)malloc(sizeof(int *) * gx);
        for (int x = 0; x < gx; x++)
        {
            visited[y][x] = (int *)malloc(sizeof(int) * 4);
            for (int d = 0; d < 4; d++)
                visited[y][x][d] = 0;
        }
    }

    // start at each node
    for (int y = 0; y < gy; y++)
    {
        for (int x = 0; x < gx; x++)
        {
            for (int sd = 0; sd < 4; sd++) // starting direction
            {
                if (!visited[y][x][sd])
                {
                    int cycle_length = 0;
                    int i = x;
                    int j = y;
                    int d = sd;
                    while (!visited[j][i][d])
                    {
                        visited[j][i][d] = 1;
                        d = (d + turn(grid[j][i])) % 4;
                        if (d < 0)
                            d += 4;
                        i = (i + move[d][0]) % gx;
                        j = (j + move[d][1]) % gy;
                        if (i < 0)
                            i += gx;
                        if (j < 0)
                            j += gy;
                        cycle_length++;
                    }

                    if (cycle_length > 0 && i == x && j == y)
                    {
                        if (cycle_lengths_cnt >= cycle_lengths_size)
                        {
                            cycle_lengths_size += 16;
                            cycle_lengths = (int *)realloc(cycle_lengths, sizeof(int) * cycle_lengths_size);
                        }
                        cycle_lengths[cycle_lengths_cnt++] = cycle_length;
                    }
                }
            }
        }
    }

    qsort(cycle_lengths, cycle_lengths_cnt, sizeof(int), cmpfunc);

    cycle_lengths = (int *)realloc(cycle_lengths, sizeof(int) * cycle_lengths_cnt);

    return cycle_lengths;
}

int main()
{
    printf("%d\n", -1 % 4);

    char *grid[2];
    size_t grid_len = 2;

    for (int i = 0; i < grid_len; i++)
    {
        grid[i] = (char *)malloc(sizeof(char) * 3);
    }
    strcpy(grid[0], "SLR");
    strcpy(grid[1], "LRR");

    int *cycle_lengths = solution(grid, grid_len);
}