/*
  Function Signature
    function magicIndex(array : array) = index : number
 */

/*
  Assumptions
    Sorted array with possible duplicate value
*/

/*

 */

function magicIndex (array, base = 0) {
  const mid = Math.floor(array.length / 2)
  if (mid === 0 && array[mid] !== mid + base) return null
  if (array[mid] === mid + base) return mid
  if (array[mid] < mid + base) return magicIndex(array.slice(mid), mid)
  if (array[mid] > mid + base) return magicIndex(array.slice(0, mid))
}
