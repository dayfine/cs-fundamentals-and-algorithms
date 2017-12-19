// Represent the inclusion of each element as 0/1 in a binary number

const powerSet = coll => {
  return Array(...Array(2 ** coll.length))
    .map((_, i) => {
      return coll.slice().filter((v, idx) => {
        return +i.toString(2).padStart(coll.length, '0')[idx]
      })
    })
}

console.log(powerSet([1, 3, 4]))
console.log(powerSet([1, 2, 3, 4, 7, 8]))
