#import .py file for cryptography
import cryptography
import communication


#global vars
url = "http://10.32.1.246:5000/blocks"
mine_url = "http://10.32.1.246:5000/mine"
walletKey = "m1y2e3x4a5m6p7l8e9w1a2l3e4t5t6k7e8y9"
minedCoins = 0
#TODO: comandline arguments? GUI?

while True:
  lastMined = int(communication.GETdata(url))
  #print lastMined
  number = cryptography.cryptoGraphy(lastMined)
  #print number
  print number
  response = communication.POSTminedJson(walletKey, number,mine_url)
  #check if the first caracter of the responce is 1 or 0, to find if we succsessfully mined a coin
  print response
  if(int(response[0])):
      minedCoins += 1
      print "Mine Sucsessful"
      print "Coins mined: " + str(minedCoins)
  else:
      print "Mine Failed"
      print "Coins mined: " + str(minedCoins)
      
      
