/*
  start from top right!
*/

function searchMatrix (matrix, target) {
  if (matrix.length === 0) return false

  let x = matrix[0].length - 1, y = 0
  while (x >= 0 && y <= matrix.length - 1) {
    if (matrix[y][x] === target) return true
    if (matrix[y][x] > target) x--
    if (matrix[y][x] < target) y++
  }

  return false
}
