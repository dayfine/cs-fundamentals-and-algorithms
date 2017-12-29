function swap (arr, i, j) {
  if (i < j) {
    const temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp
  }
}

function partition (arr, low, high) {
  let i = low - 1, j = low, pivot = arr[high]
  for (;j < high; j++) {
    if (arr[j] <= pivot) {
      i++
      swap(arr, i, j)
    }
  }
  i++
  swap(arr, i, high)
  return i
}

function quickSort (arr, low = 0, high = arr.length - 1) {
  if (low === 0 && high === 0) return arr

  if (low < high) {
    let piv = partition(arr, low, high)
    quickSort(arr, low, piv - 1)
    quickSort(arr, piv + 1, high)
  }

  return arr
}

// console.log(quickSort([1,3,2,7,5,4,5,3,4,1,6,8,3,2,2,4,1,6,7,2]))
