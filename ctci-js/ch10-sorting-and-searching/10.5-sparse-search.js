/*
  ["", "ans", "", "", "", "ncd", "", "", "z"]
*/

function sparseSearch (arr, target) {
  let lo = 0, hi = arr.length - 1

  while (lo <= high) {
    let mid = Math.floor((lo + hi) / 2)

    if (arr[mid] === '') {
      let left = mid - 1, right = mid + 1

      while (true) {
        if (left < lo && right > hi) {
          return -1
        } else if (left >= lo && arr[left] !== '') {
          mid = left
          break
        } else if (right <= hi && arr[right] !== '') {
          mid = right
          break
        }
      }
    }
    continue
  } else if (arr[mid] > target) {
    hi = mid - 1
  } else if (arr[mid] < target) {
    lo = mid + 1
  } else {
    return mid
  }

  return -1
}
