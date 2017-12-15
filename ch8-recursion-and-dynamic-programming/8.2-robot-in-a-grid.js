// Untested

/*
  Function Signature
    function route(map: array of array) = array-of-steps
 */

/*
  Assumptions:
    Assuming map is an array of array, where each element is either true or false,
    representing whether the cell is accessible, i.e. not 'off limit'
*/

/*
  Test cases:
 */

function route (map) {
  const exitX = map.length
  const exitY = map[0].length
  const visited = {}

  function findExit (x, y, path) {
    if ((x === exitX) && (y === exitY)) return path

    if (!map[x] || !map[x][y] || visited[`${x}&${y}`]) return

    visited[`${x}&${y}`] = true

    return findExit(x + 1, y, path.concat('down')) ||
           findExit(x, y + 1, path.concat('right'))
  }

  return findExit(0, 0, [])
}
