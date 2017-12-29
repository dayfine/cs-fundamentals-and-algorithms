function rotatedSearch (arr, num, left = 0, right = arr.length - 1) {
  let mid = Math.floor((left + right) / 2)
  if (arr[mid] === num) return mid

  if (right < left) return -1

  if (arr[left] < arr[mid]) {
    // left half is sorted, i.e. right half is not
    if (arr[left] <= num && num < arr[mid]) {
      return rotatedSearch(arr, num, left, mid - 1)
    } else {
      return rotatedSearch(arr, num, mid + 1, right)
    }
  } else if (arr[mid] < arr[right]) {
    // right half is sorted, i.e. left half is not
    if (arr[mid] < num && num <= arr[right]) {
      return rotatedSearch(arr, num, mid + 1, right)
    } else {
      return rotatedSearch(arr, num, left, mid - 1)
    }
  } else {
    // tricky duplicate: can't tell where is the break point
    if (arr[left] === arr[mid] && arr[mid] !== arr[right]) {
      // right half is NOT sorted, and left half is duplicates
      // search right half
      return rotatedSearch(arr, num, mid + 1, right)
    } else if (arr[right] === arr[mid] && arr[mid] !== arr[left]) {
      // left half is NOT sorted, and right half is duplicates
      // search left half
      return rotatedSearch(arr, num, left, mid - 1)
    } else {
      // needs to try both
      return Math.max(
          rotatedSearch(arr, num, left, mid - 1),
          rotatedSearch(arr, num, mid + 1, right)
        )
    }
  }
}

// console.log(rotatedSearch([2], 2))
// console.log(rotatedSearch([1,2],2))
// console.log(rotatedSearch([3,3,3,3,4,5],4))
// console.log(rotatedSearch([3,3,3,3,4,5],2))
// console.log(rotatedSearch([0,1,2,3,4,5],5))
// console.log(rotatedSearch([1,2,3,4,5,0],3))
// console.log(rotatedSearch([9,12,17,2,4,5],12))
// console.log(rotatedSearch([9,12,17,2,4,5,6],4))

// modified BSI version
function rotatedSearch2 (shiftArr, num, offset = 0) {
  if (shiftArr.length < 1) return -1
  if (shiftArr.length === 1) return shiftArr[0] === num ? offset : -1

  let midpoint = Math.floor(shiftArr.length / 2)

  if (shiftArr[0] < shiftArr[shiftArr.length - 1]) {
    return offset + bsi(shiftArr, num)
  } else {
    return Math.max(
      rotatedSearch2(shiftArr.slice(0, midpoint), num, offset),
      rotatedSearch2(shiftArr.slice(midpoint), num, midpoint + offset)
    )
  }
}

function bsi (arr, num) {
  if (arr.length < 0) return -1
  let start = 0, end = arr.length

  while (start < end - 1) {
    let midpoint = Math.floor((start + end) / 2)
    if (num < arr[midpoint]) {
      end = midpoint
    } else if (num > arr[midpoint]) {
      start = midpoint
    } else {
      return midpoint
    }
  }

  return -1
}
