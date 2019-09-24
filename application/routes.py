from flask import Flask, request, session, redirect, render_template
from twilio.twiml.messaging_response import MessagingResponse, Message, Body
from twilio.rest import Client
import geocoder
import json
import requests
import urllib.request
from application import app

SECRET_KEY = 'a secret key'
app.config.from_object(__name__)
GOOGLE_API_KEY=<MY_SECRET_KEY>


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/getwhat', methods=['GET', 'POST'])
def getwhat():
    resp = MessagingResponse()
    from_number = request.values.get('From', None)
    number = from_number
    
    counter = session.get('counter', 0)
    #counter = 0
    counter += 1
    # Save the new counter value in the session
    session['counter'] = counter
    print(str(from_number) + " Counter = " + str(counter))
    out_string = ""
    
    if counter == 1:
        out_string = out_string + "Hello and welcome to 1800-GETWHAT!\n\n"
        out_string = out_string + "Please enter what you want to look for, the location of your search, "
        out_string = out_string + "and the radius of your search in miles (no units) separated by commas and a space."
        out_string = out_string + "\nFor example: ATM, 20057, 0.5  OR  Grocery Stores, The White House, 2"

    #print(out_string)

    #elif counter%3 == 2:  # respond with invalid keyword
    #searchInput = request.values.get('Body', None)
    #out_string ="Please enter a location (address, zip code, neighborhood, etc.) where you would like to find "
    #out_string = out_string + searchInput

    else:
        searchInput = request.values.get('Body', None)
        inputs = searchInput.split(', ')
        if len(inputs) < 3:
            resp.message("Please enter your information in the correct format:\n(Search, Location, Radius)")
            return str(resp)
        mySearch = str(inputs[0])
        replacedSearch = mySearch.replace(' ', '%20')
        print(mySearch)
        myAddress = str(inputs[1])
        myRadius = str(float(inputs[2])*1600)

        g = geocoder.google(myAddress, key=GOOGLE_API_KEY)
        print(g.latlng)
        search = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(g.lat) + ',' + str(g.lng) + '&radius=' + myRadius + '&type=' + replacedSearch
        search = search + '&keyword=' + replacedSearch
        search = search + '&fields=name,formatted_address,vicinity&key=' + GOOGLE_API_KEY
            #print("Flag 1")
            
            #search = 'https://maps.googleapis.com/maps/api/pslace/findplacefromtext/json?input=ATM&inputtype=textquery&fields=name,formatted_address&locationbias=circle:2000@' + str(g.lat) + ',' + str(g.lng) + '&key=' + GOOGLE_API_KEY
        print(search)
        
        with urllib.request.urlopen(search) as url:
                data = json.loads(url.read().decode())
        #print("Flag 3")
        result_list = len(data["results"])
            #print(result_list)
        out_string = "For " + mySearch + " around " + myAddress + " in a " + inputs[2] + " mile radius:\n\n"
            #print("Flag 2")
        for x in range(0, result_list):
            out_string += (data["results"][x]["name"]) + " – "
            out_string += (data["results"][x]["vicinity"]) + "\n\n"

    #print(data)
    #print(search)
    #data = json.loads(json_data)
    #json.dumps(data, indent=4, separators=(',', ': '))
    #print(type(data))
    #print(data)

    resp.message(out_string)
    return str(resp)

#if __name__=="__main__":
#app.run(debug=True)


