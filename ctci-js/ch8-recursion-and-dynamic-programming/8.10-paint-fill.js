function fill (screen, [x, y], color) {
  const oldColor = screen[x][y]
  const row = screen.length
  const col = screen[0].length

  function paint ([x, y]) {
    ;[[0, 1], [0, -1], [1, 0], [-1, 0]].forEach(([_x, _y]) => {
      const xi = x + _x
      const yi = y + _y

      if (xi >= 0 && xi < row && yi >= 0 && yi < col && screen[xi][yi]) {
        screen[xi][yi] = color
        paint([xi, yi])
      }
    })
  }

  screen[x][y] = color
  paint([x, y])
}
