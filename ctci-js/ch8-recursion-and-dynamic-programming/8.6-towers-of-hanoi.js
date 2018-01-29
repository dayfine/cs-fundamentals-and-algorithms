/*
  Using the three stacks/towers to move all rings from stack1 to stack 3
  function ToH(stacks: stacks, numOfRings: number) => (stacks: stacks)
*/

/*
  Assumptions:
    Using stack, e.g. pop, push, peek?
*/

/*
  Runtime:
    O(2^n)
*/

/*
  Approach:
    start with simple case: n = 2
      stacks: init, helper, target
      1: init => helper
      2: init => target
      1: helper => target

    start with another simple case: n = 3
      stacks: init, helper, target
      1: init => target
      2: init => helper
      1: target => helper
      3: init => target
      1: helper => init
      2: helper => target
      1: init => target
      Seven steps

      ToH(3, i, h, t) = ToH(2, i, t, h), 3it, ToH(2, h, i, t)
*/

function ToH (n, i, h, t) {
  if (n === 1) {
    t.push(i.pop())
  } else if (n === 2) {
    h.push(i.pop())
    t.push(i.pop())
    t.push(h.pop())
  } else {
    ToH(n - 1, i, t, h)
    t.push(i.pop())
    ToH(n - 1, h, i, t)
  }
}
