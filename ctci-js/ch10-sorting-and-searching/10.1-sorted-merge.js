/*
  a is longer with enough spaces at the end
*/

function merge (a, b) {
  // make space only
  //   a = a.concat(b)
  // or
  //   let bi = b.length
  //   while (--bi >= 0) {a.push(null)}

  let ai = a.length - 1, bi = b.length, target = ai + bi - 1

  while (bi >= 0) {
    a[target--] = ai >= 0 && a[ai] > b[bi]
                    ? a[ai--]
                    : b[bi--]
  }
}
