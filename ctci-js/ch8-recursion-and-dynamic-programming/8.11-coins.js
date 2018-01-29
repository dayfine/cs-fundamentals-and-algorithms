function countChange (money, coins, m = coins.length) {
    // If n is 0 then there is 1 solution (do not include any coin)
  if (money == 0) return 1

    // If n is less than 0 then no solution exists
  if (money < 0) return 0

    // If there are no coins and n is greater than 0, then no solution exist
  if (m <= 0 && money >= 1) return 0

    // count is sum of solutions (i) including S[m-1] (ii) excluding S[m-1]
  return countChange(money, coins, m - 1) + countChange(money - coins[m - 1], coins, m)
}
