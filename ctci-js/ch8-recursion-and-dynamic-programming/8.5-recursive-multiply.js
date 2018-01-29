/*
  Signature
    > function multiply(a: number, b: number)=> output: number
*/

/*
  Assumption
    > Positive integers
    > Plus and Minus or Bitwise Operators
    > Presumbly using recursion
*/

/*
Examples
  a * b
    4321 * 9831 => adding multiple times
    1 * 9831 > b by n times where n < 10, m
    2 * 9831 + '0' > b by n times where n < 10, m  9831+ 9831
    3 * 9831 + '00' > b by n times where n < 10, m
    4 * 9831 + '000' > b by n times where n < 10, m
*/

/*
Runtime
  add a by b times
    > smaller (a | b)
  digit by digit
    > a.length * constant (expected: < 10)

  divide and conquer
    > log(a)
*/

/*
  Solution
*/

function multiply (a, b, trailingZeros = 0, memo = {}) {
  // base case
  if (a === 0) return 0

  let min, max, multiplyer, next, temp = 0

  // only for the initial run
  if (trailingZeros === 0) {
    min = a < b ? a : b // 4321
    max = a < b ? b : a
  } else {
    min = a
    max = b
  }

  multiplyer = min % 10 // 1
  next = Math.floor(min / 10) // 432

  // caching / retrieving
  if (memo[multiplyer]) {
    temp = memo[multiplyer]
  } else {
    for (let j = 0; j < multiplyer; j++) temp += max
    memo[multiplyer] = temp
  }

  // Appending zeros
  temp = temp.toString() + '0'.repeat(trailingZeros)

  trailingZeros++

  return Number(temp) + multiply(next, max, trailingZeros, memo)
}

console.log(multiply(4312327142, 2214))

/*
  Recursive solution 2 (Credit to Tim Kao)
*/

function recursiveMultiply (numA, numB) {
  const smaller = numA <= numB ? numA : numB
  const bigger = numA > numB ? numA : numB

  return smaller % 2 === 1
    ? multiplyHelper(smaller - 1, bigger) + bigger
    : multiplyHelper(smaller, bigger)
}

function multiplyHelper (smaller, bigger) {
  // base case and optimazation
  if (smaller === 0) return 0
  if (smaller === 1) return bigger

  // calculate one side and add twice
  const divideSmaller = smaller >> 1
  const side1 = multiplyHelper(divideSmaller, bigger)

  return side1 + side1
}
