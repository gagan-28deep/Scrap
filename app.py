from flask import Flask , render_template  ,request , jsonify
from flask_cors import CORS , cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route("/" , methods = ['POST' , 'GET'])
@cross_origin()
def homepage():
    return render_template('index.html')

@app.route("/scrap" , methods = ["POST" , "GET"])
def index():
    if request.method =="POST":
        searchString = request.form['content'].replace(" " , "")
        try:
            URL = "https://www.passiton.com/inspirational-quotes?q=" + searchString
            uClient = uReq(URL)
            URL_page = uClient.read()
            uClient.close()
            Page_html = bs(URL_page , "html.parser")
            bigboxes = Page_html.findAll("div",{"class": "col-6 col-lg-3 text-center margin-30px-bottom sm-margin-30px-top"})
            box = bigboxes[0]
            quote = []
            for box in bigboxes:
                try:
                    theme = box.h5.text
                except:
                    return "No Theme"
                try:
                    quote_img_text = box.img['alt'].split(" #")[0]

                except:
                    quote_img_text = 'No Text'

                try:
                    lines = box.p.text
                except:
                    lines = "No Lines"

                try:
                    author = box.div.small.text
                except:
                    author = 'No Author'
                mydict = {"Product": searchString, "Theme": theme, "Quote_Img_text": quote_img_text, "Lines" : lines ,"Author": author}
                quote.append(mydict)
            return render_template('results.html' , quotes = quote)
        except:
            return "Smething is wrong"




if __name__ == '__main__':
    app.run(port=8000 , debug=True)