#!/usr/bin/python3
import boto3
from flask import Flask,render_template,request
import json
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

lambda_region = ''
lambda_function_name = ''
invokeLam = boto3.client("lambda", region_name = lambda_region)

try:
    response = invokeLam.invoke(FunctionName = lambda_function_name , InvocationType = "RequestResponse", Payload="")
except Exception as err:
    print(err)

# Running the Web Application
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    return render_template("index")

@app.route("/index", methods=["GET","POST"])
def return_home():
    return render_template("index")

@app.route("/decrypt",methods=["POST"])
def decryption():
    if request.form :
        user_password = request.form.get('enc_password')
        process_identifier = request.form.get('process_identifier')
        if user_password:
            payload={"user_password": user_password,"process_identifier": process_identifier,"flag": 0}
            try:
                response = invokeLam.invoke(FunctionName = lambda_function_name, InvocationType = "RequestResponse", Payload = json.dumps(payload))
                decoded_text=eval(response['Payload'].read().decode())['decrypted_password']
                message="Decrypted password : {}".format(decoded_text)
                return(message)

            except Exception as e:
                return("Wrong Password Entered. Please try again by clicking <a href='index'>here</a> . ")
    
        else:
            return("Password field is blank. Please try again by clicking <a href='index'>here</a>. ")
    else:
        return render_template("404.html"),404


@app.errorhandler(404)
def not_found(e):
  return render_template("404.html"),404

if __name__ == "__main__":
    app.run(host='0.0.0.0')
