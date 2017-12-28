/*
  LC 49
  Given an array of strings, group anagrams together.

  For example, given: ["eat", "tea", "tan", "ate", "nat", "bat"],
  Return:

  [
    ["ate", "eat","tea"],
    ["nat","tan"],
    ["bat"]
  ]
*/

function groupAnagrams (strs) {
  if (!strs.length) return []

  const groups = {}

  for (let i = 0; i < strs.length; i++) {
    const hash = strs[i] === ''
      ? strs[i]
      : strs[i].split('').sort().join('')

    if (groups[hash]) groups[hash].push(strs[i])
    else groups[hash] = [strs[i]]
  }

  return Object.values(groups)
}
