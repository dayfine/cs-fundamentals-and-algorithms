/*
  Assumptions:
    Listy is a list of unknown size filled with sorted positive integers
    elementAt(i) method can give the number at index i or -1 if it's beyond range
*/

function noSizeSearch (n, Listy) {
  // get size
  let size = 1
  while (Listy.elementAt(size) > 0) {
    size *= 2
  }

  let lo = 0, hi = size - 1

  while (lo <= hi) {
    let mid = Math.floor((lo + hi) / 2)

    if (Listy.elementAt(mid) === n) {
      return mid
    } else if (Listy.elementAt(mid) > n ||
               Listy.elementAt(mid) === -1
    ) {
      hi = mid
    } else {
      lo = mid - 1
    }
  }

  return -1
}
