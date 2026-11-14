/* Necati Selcuk, 5001240039, G2 - Exam grade distribution (4g: passes 1-2 merged) */

#define N 38
const int SID = 1240039;

int grades[N];
int bucket[5];
int mean;
int below_count;
int pass_count;

/* returns range index 0..4 */
int bucket_of(int v)
{
    if (v < 50) return 0;
    if (v < 65) return 1;
    if (v < 75) return 2;
    if (v < 85) return 3;
    return 4;
}

/* flags grade with bit 8 if below mean */
int mark(int v, int m)
{
    if (v < m) return v | 0x100;
    return v;
}

int main(void)
{
    unsigned int x = SID;
    int sum = 0;

    /* pass 1: generate grades, count ranges, passing grades and sum */
    for (int i = 0; i < N; i++) {
        x = 1664525u * x + 1013904223u;
        int v = (x >> 16) % 101;
        grades[i] = v;
        bucket[bucket_of(v)]++;
        if (v >= 59) pass_count++;
        sum += v;
    }
    mean = sum / N;

    /* pass 2: flag grades below mean */
    for (int i = 0; i < N; i++) {
        int f = mark(grades[i], mean);
        if (f != grades[i]) below_count++;
        grades[i] = f;
    }

    return 0;
}