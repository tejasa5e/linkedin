from flask import *
from DBM_LINKEDIN import Add_name, Get_name, Add_link, Get_links, to_data
#import json
#import pandas as pd


app=Flask(__name__)


@app.route("/")#sample page for name input
def input():
    return render_template("input.html")


@app.route("/Add_name",methods=["POST"])# to add name in database
def Add_Name():
    name=request.form.get("Ename")
    t=(name)
    Add_name(t)
    return redirect ("/profil")

@app.route("/profil")#to get all profiles of same name from linkedin
def Get_profile():
    res=to_data()
    return render_template("links.html")

@app.route("/get_response",methods=['POST','GET'])#to get link of specific profile
def Get_response():
    link=request.form['Link']
    name=request.form['Name']
    l=(link,name)
    Add_link(l)
    return None




    

if(__name__=="__main__"):
    app.run(debug=True)
