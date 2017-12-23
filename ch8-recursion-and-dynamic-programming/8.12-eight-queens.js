function eightQueens () {
  const coll

  const Queens = []


   for (let i; i; i++)

  function buildBoard (Queens=[]) {
    if (Queens.length===8)  coll.push(Queens)
    const valid = (row, col) => Queens.every((cv, ci) =>
      cv !== col && Math.abs(ci - row) !== Math.abs(cv - col)
    )


  }


  return coll
}
