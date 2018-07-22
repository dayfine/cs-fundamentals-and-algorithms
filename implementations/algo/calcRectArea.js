function calculate (recs) {
  // the (unique) left and ride edges
  const criticalPoints = [...new Set([].concat(...recs.map(_ => [_[0], _[2]])))]

  // left to right
  recs = recs.sort((a, b) => a[0] - b[0])

  let totalArea = 0
  let offset = 0
  let activeRecs = []

  criticalPoints
    .sort((a, b) => a - b)
    .reduce((prevStep, currStep) => {
      let heightUnit = 0
      activeRecs
        .sort((a, b) => a[1] - b[1]) // top to bottom
        .reduce((prev, cur) => {
          // how many unit of heights to include?
          if (prev < cur[3]) {
            heightUnit += cur[3] - Math.max(cur[1], prev)
            return cur[3]
          }
          return prev
        }, 0)
      // unit of height * difference in width
      totalArea += heightUnit * (currStep - prevStep)

      // remove those rectangle whose right edge is lte this coord
      activeRecs = activeRecs.filter(r => r[2] > currStep)

      let i = offset
      // add those rectangles that have left edges at this coord
      while (recs[i] && recs[i][0] === currStep) {
        activeRecs.push(recs[i++])
        offset = i
      }
      return currStep
    }, 0)

  return totalArea
}
