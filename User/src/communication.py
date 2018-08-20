#file for data communication

#import lib for url get & post requests
import urllib2
import json

#function for getting data from server
def GETdata(url):
  #simply returns processed string
  return urllib2.urlopen(url).read()

#function for sending data to server
def POSTminedJson(minerKey, result,url):
    #convert data into JSON
    data = json.dumps({ "miner":str(minerKey), 
            "number":str(result)})
    #send request, we have to tell the server the content type
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    #get a responce
    responce = urllib2.urlopen(req)
    #read it
    responce = responce.read()
    #print it
    return responce
    
