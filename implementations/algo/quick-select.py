def partition(arr, lo, hi):
    pivot = arr[lo]
    i, j = lo + 1, hi

    while i <= j:
        if arr[i] > pivot and arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
        while i <= j and arr[i] <= pivot:
            i += 1
        while i <= j and arr[j] >= pivot:
            j -= 1

    arr[lo] = arr[j]
    arr[j] = pivot
    return j

def quick_select_kth_smallest(arr, k):
    left, right = 0, len(arr) - 1

    while True:
        pivot_idx = partition(arr, left, right)
        if pivot_idx == k - 1:
            return arr[k - 1]
        elif pivot_idx > k - 1:
            right = pivot_idx - 1
        else:
            left = pivot_idx + 1

test_arr = [1, 2, 3, 3, 99, 2, 3, 1, 7, 12, 17, 19, 23, -1, -5, 81, 23]

print(quick_select_kth_smallest(test_arr[:], 1))
print(quick_select_kth_smallest(test_arr[:], 2))
print(quick_select_kth_smallest(test_arr[:], 3))
print(quick_select_kth_smallest(test_arr[:], 4))
print(quick_select_kth_smallest(test_arr[:], 5))
print(quick_select_kth_smallest(test_arr[:], 6))
print(quick_select_kth_smallest(test_arr[:], 7))
print(quick_select_kth_smallest(test_arr[:], 8))
print(quick_select_kth_smallest(test_arr[:], 9))
print(quick_select_kth_smallest(test_arr[:], 10))

def partition_large(nums, lo, hi):
    pivot = nums[lo]
    i, j = lo + 1, hi

    while i <= j:
        if nums[i] < pivot and nums[j] > pivot:
            nums[i], nums[j] = nums[j], nums[i]
        while i <= j and nums[i] >= pivot:
            i += 1
        while i <= j and nums[j] <= pivot:
            j -= 1

    nums[lo] = nums[j]
    nums[j] = pivot
    return j

def quick_select_kth_largest(arr, k):
    left, right = 0, len(arr) - 1

    while True:
        pivot_idx = partition_large(arr, left, right)
        if pivot_idx == k - 1:
            return arr[k - 1]
        elif pivot_idx > k - 1:
            right = pivot_idx - 1
        else:
            left = pivot_idx + 1


print(quick_select_kth_largest(test_arr[:], 1))
print(quick_select_kth_largest(test_arr[:], 2))
print(quick_select_kth_largest(test_arr[:], 3))
print(quick_select_kth_largest(test_arr[:], 4))
print(quick_select_kth_largest(test_arr[:], 5))
print(quick_select_kth_largest(test_arr[:], 6))
print(quick_select_kth_largest(test_arr[:], 7))
print(quick_select_kth_largest(test_arr[:], 8))
print(quick_select_kth_largest(test_arr[:], 9))
print(quick_select_kth_largest(test_arr[:], 10))

# errr list index out of range!
print(quick_select_kth_largest([1, 2, 5, 3, 2], 1))
print(quick_select_kth_largest([1, 2, 5, 3, 2], 2))
print(quick_select_kth_largest([1, 2, 5, 3, 2], 3))
print(quick_select_kth_largest([1, 2], 1))
print(quick_select_kth_largest([1, 2], 2))
