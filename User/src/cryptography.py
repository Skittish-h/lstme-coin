#File for Cryptographic algorithms
def cryptoGraphy(lastDifficulty):
  # Create a variable that we will use to find
  # our next proof of work
  incrementor = lastDifficulty + 1
  while not (incrementor % 9 == 0 and incrementor % lastDifficulty == 0):
    incrementor += 1
  # Once that number is found,
  # we can return it as a proof
  # of our work
  return incrementor
