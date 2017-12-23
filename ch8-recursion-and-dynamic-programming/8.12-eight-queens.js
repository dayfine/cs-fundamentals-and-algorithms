function eightQueens () {
  const coll = []

  function buildBoard (Queens = []) {
    if (Queens.length === 8) coll.push(Queens)

    const valid = (row, col) => Queens.every((cv, ci) =>
      cv !== col && Math.abs(ci - row) !== Math.abs(cv - col)
    )

    let r = Queens.length

    for (let c = 0; c < 8; c++) {
      if (valid(r, c)) buildBoard([...Queens, c])
    }
  }

  buildBoard()

  return coll
}

eightQueens()
