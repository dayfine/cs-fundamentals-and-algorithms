def partition(arr, lo, hi):
    pivot = arr[lo]
    i, j = lo, hi

    while i < j:
        while i <= hi and arr[i] < pivot:
            i += 1
        while arr[j] > pivot:
            j -= 1
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]

    arr[lo] = arr[j]
    arr[j] = pivot

    return j

def quick_sort(arr, lo, hi):
    if hi > lo:
        pivot_idx = partition(arr, lo, hi)
        quick_sort(array, lo, pivot_idx - 1)
        quick_sort(array, pivot_idx + 1, hi)

def quick_sort_main(arr):
    quick_sort(arr, 0, len(arr) - 1)
