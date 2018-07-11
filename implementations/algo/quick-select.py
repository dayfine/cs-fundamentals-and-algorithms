def partition(arr, lo, hi):
    pivot = arr[lo]
    i, j = lo + 1, hi

    while i <= j:
        while arr[i] <= pivot:
            i += 1
        while arr[j] >= pivot:
            j -= 1
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1

    arr[lo] = arr[j]
    arr[j] = pivot
    return j

def quick_select_kth_smallest(arr, k):
    left, right = 0, len(arr) - 1

    while True:
        pivot_idx = partition(arr, left, right)
        if k == pivot_idx:
            return arr[k]
        elif k < pivot_idx:
            right = pivot_idx - 1
        else:
            left = pivot_idx + 1

arr = [1, 2, 3, 3, 99, 2, 3, 1, 7, 12, 17, 19, 23, -1, -5]
print(quick_select_kth_smallest(arr[:], 0))
print(quick_select_kth_smallest(arr[:], 1))
print(quick_select_kth_smallest(arr[:], 2))
print(quick_select_kth_smallest(arr[:], 3))
print(quick_select_kth_smallest(arr[:], 4))
print(quick_select_kth_smallest(arr[:], 5))
print(quick_select_kth_smallest(arr[:], 6))
print(quick_select_kth_smallest(arr[:], 7))
print(quick_select_kth_smallest(arr[:], 8))
print(quick_select_kth_smallest(arr[:], 9))
print(quick_select_kth_smallest(arr[:], 10))
