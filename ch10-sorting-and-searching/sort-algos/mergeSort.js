function merge (arr1, arr2) {
  const ret = []
  let i1 = 0, i2 = 0

  while (i1 < arr1.length || i2 < arr2.length) {
    if (arr1[i1] < arr2[i2] || i2 === arr2.length) {
      ret.push(arr1[i1++])
    } else {
      ret.push(arr2[i2++])
    }
  }
  return ret
}

function mergeSort (arr) {
  if (arr.length < 2) return arr

  const mid = Math.floor(arr.length / 2)

  return merge(
      mergeSort(arr.slice(0, mid)),
      mergeSort(arr.slice(mid))
    )
}

// console.log(mergeSort([1,3,2,7,5,4,5,3,4,1,6,8,3,2,2,4,1,6,7,2]))
