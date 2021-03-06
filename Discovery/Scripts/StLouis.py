""" 
--------------------------------------------------------------------------------
Descriptive Name     : StLouis.py
Author               : unknown								      
Contact Info         : cwengyan@purdue.edu (Chan Weng Yan)
Date Written         : unknown
Description          : Parse cameras on the St. Louis Department of Transportation traffic camera website
Command to run script: python StLouis.py
Output               : output urls, country, city and latitude, longitude to a 
                       textfile <list_stlouis>
Note                 : It will utilize selenium webdriver to deal with html source code generated by javascript. 
                       It will then implement Regex to extract the relevant information and use Google API to 
                       convert street addresses to geo locations.
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.gatewayguide.com/
In database (Y/N)    : N
Date added to Database : unknown
--------------------------------------------------------------------------------
"""
from selenium import webdriver
import urllib2
import re
import json
import time

def getSTL():
    #Use webdriver to fetch website and find camera list element
    file = open('list_StLouis.txt','w')
    driver = webdriver.Firefox()
    driver.get("http://www.gatewayguide.com/")
    time.sleep(10)
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="cc"]/table[1]/tbody/tr/td/iframe'))
    html=driver.find_element_by_id("cmbCameras")
    #Extract nested HTML
    elem=html.get_attribute('innerHTML')

    imglist=[]
    streetlist=[]
    latlist=[]
    lnglist=[]

    #Use regex to extract image urls
    images=re.findall(r'full=".*?"', elem)
    for ind in images:
        match=re.search(r'full="(.*?)"', ind)
        imgurl=match.group(1)
        imglist.append(imgurl)

    #Use regex to extract street addresses
    streets=re.findall(r'">.*?</option>', elem)
    for ind in streets:
        match=re.search(r'">(.*?)</option>', ind)
        street=match.group(1)
        if '@' in street:
            street=street.replace('@','at')
        if street.count('/') >= 2:
            streetgroup = street.split('/')
            street='/'.join(streetgroup[:2])
        streetlist.append(street)
        #Format and run through Google API
        line = street.replace(" ","+")
        line1 = line.strip()
        add = line1+'+'+'St.Louis'
        api = 'http://maps.googleapis.com/maps/api/geocode/json?address='+add
        response = urllib2.urlopen(api).read()
        #Load by json module
        parsed_json = json.loads(response)
        content = parsed_json['results']
        #Extract latitude and longitude from the API json code
        loc = content[0]
        geo = loc['geometry']
        location2 = geo['location']
        lat = location2['lat']
        lng = location2['lng']
        string_lat = str(lat)
        string_lng = str(lng)
        latlist.append(string_lat)
        lnglist.append(string_lng)
        time.sleep(0.1)

    #Write output to file
    iter=0
    while iter < len(imglist):
        output = streetlist[iter]+'#'+'St.Louis'+'#'+'MO'+'#'+'USA''#'+imglist[iter]+'#'+latlist[iter]+'#'+lnglist[iter]
        iter +=1
        file.write(output.encode('utf-8')+'\n')

    file.close()

if __name__ == "__main__":
    getSTL()
