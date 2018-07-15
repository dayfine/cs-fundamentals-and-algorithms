from collections import deque

def merge_sort_main(arr):
    return merge_sort(arr, 0, len(arr)-1)

def merge_sort(arr, low, high):
    if low < high:
        middle = (low + high) // 2
        merge_sort(arr, low, middle)
        merge_sort(arr, middle + 1, high)
        merge(arr, low, middle, high)

def merge(arr, low ,middle, high):
    q1, q2 = deque(arr[low:middle+1]), deque(arr[middle+1:high+1])

    i = low
    while q1 and q2:
        if q1[0] <= q2[0]:
            s[i] = q1.popleft()
        else:
            s[i] = q2.popleft()
        i += 1

    while q1:
        s[i] = q1.popleft()
        i += 1

    while q2:
        s[i] = q2.popleft()
        i += 1
