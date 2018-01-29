/*
  boxes: array of boxes
  box [height, width, depth]
*/

function getMaxHeight (boxes) {
  // [height, width, depth]
  boxes.sort((arr1, arr2)=>arr1[1]-arr2[1])
  // array of boxes sorted by width from low to high

  function buildStack(boxes, height=0) {
    if (boxes.length===0) return height

    let largest = boxes[boxes.length - 1]

    const smaller = boxes.filter(box=>box[1]<largest[1] && box[2] < largest[2])
    const notSmaller  = boxes.filter(box=>(box[1]>=largest[1] || box[2] >= largest[2]) && box !== largest)

    return Math.max(
      buildStack(smaller, height+largest[0]),
      buildStack(notSmaller, height)
    )
}
