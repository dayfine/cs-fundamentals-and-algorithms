/*
  function permu (string: string) => array of strings
*/

/*
  Assumptions:
    All unique characters
*/

/*
  Runtime:
    O(2^n)
*/

function permu (string) {
  const coll = []

  let characters = string.split('')

  function build (chars, partial = '') {
    if (chars.length === 0) {
      coll.push(partial)
      return
    }
    for (let i = 0; i < chars.length; i++) {
      let _chars = chars.slice()
      _chars.splice(i, 1)
      build(_chars, partial + chars[i])
    }
  }

  build(characters)

  return coll
}

/*
  Test
    console.log(permu('adbc'))
*/
