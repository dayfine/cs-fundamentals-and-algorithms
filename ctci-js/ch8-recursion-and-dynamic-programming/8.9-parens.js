function parens (n) {
  let coll = []

  function build (l = 0, r = 0, partial = '') {
    if (l === n && r === n) return coll.push(partial)
    if (l < n) build(l + 1, r, `${partial}(`)
    if (r < l) build(l, r + 1, `${partial})`)
  }

  build()

  return coll
}

// console.log(parens(1))
// console.log(parens(2))
// console.log(parens(3))
