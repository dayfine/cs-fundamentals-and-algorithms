/*
  Function Signature
    function steps(integer n, array memo) = integer combination-of-steps
 */

/*
  Assumptions
    Non-polynomial run-time
*/

/*
  Test cases:
    3 => 4 (1-1-1, 2-1, 1-2, 3)
    4 => 7 (1-1-1-1, 1-1-2, 1-2-1, 1-3, 2-1-1, 2-2, 3-1)
    5 => 13 (1-1-1-1-1, 1-1-1-2, 1-1-2-1, 1-1-3, 1-2-1-1, 1-2-2, 1-3-1, 2-1-1-1,
             2-1-2, 2-2-1, 2-3, 3-1-1, 3-2)

    100 => something really large
 */

function steps (n, memo = []) {
  if (n === 1) return 1 // 1
  if (n === 2) return 2 // 1-1, 2
  if (n === 3) return 4 // 1-1-1, 2-1, 1-2, 3

  if (!memo[n]) {
    memo[n] = [1, 2, 3].reduce((sum, ni) => sum += steps(n - ni, memo), 0)
  }

  return memo[n]
}

// Tests
// console.log(steps(3))
// console.log(steps(4))
// console.log(steps(5))
// console.log(steps(100))
