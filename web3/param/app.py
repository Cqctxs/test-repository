import os
from flask import Flask, request, render_template, redirect
import requests
import json
app = Flask(__name__, static_url_path="/static")

flag = os.environ.get("FLAG")
# this is so scuffed .-.
os.system("apachectl start")

@app.route("/")
def send_money():
    response = requests.get("http://localhost:80/gateway.php").content
    accounts = json.loads(response)
    return render_template("send-money.html", data=accounts)

@app.route("/check-balance", methods=["GET"])
def check():
    response = requests.get("http://localhost:80/gateway.php").content
    accounts = json.loads(response)

    if (accounts["Eatingfood"] < 0):
        return render_template("check-balance.html", data=accounts, flag=":(")
    if (accounts["Eatingfood"] >= 100000):
        return render_template("check-balance.html", data=accounts, flag=flag)
    return render_template("check-balance.html", data=accounts)

@app.route("/send", methods=["POST"])
def send_data():
    raw_data = request.get_data()
    recipient = request.form.get("recipient");
    amount = request.form.get("amount");

    if (amount == None or (not amount.isdigit()) or int(amount) < 0 or recipient == None or recipient == "Eatingfood"):
        return redirect("https://media.tenor.com/UlIwB2YVcGwAAAAC/waah-waa.gif")
    
    # Send the data to the Apache PHP server
    raw_data = b"sender=Eatingfood&" + raw_data;
    requests.post("http://localhost:80/gateway.php", headers={"content-type": request.headers.get("content-type")}, data=raw_data)
    return redirect("/check-balance")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
