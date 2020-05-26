from flask import Flask, render_template, redirect
from flask import send_from_directory
from flask_dynamo import Dynamo
from flask import request, jsonify
import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr
from passlib.context import CryptContext

app = Flask(__name__)
pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)
SENDER = "travelsite22@gmail.com"
#RECIPIENT = "saratsss70@gmail.com"
AWS_REGION = "us-east-1"
SUBJECT = "Welcome to Travelsite"

#BODY_TEXT = ("Amazon SES Test (Python)\r\n"
#             "This email was sent with Amazon SES using the "
#             "AWS SDK for Python (Boto)."
#            )

BODY_TEXT = ("Welcome to Travel Website"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )


BODY_HTML = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
            """


CHARSET = "UTF-8"
client = boto3.client('ses',region_name=AWS_REGION)
dynamo_client = boto3.client('dynamodb',region_name=AWS_REGION)
dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
table = dynamodb.Table('users')
searchTable = dynamodb.Table('search')



@app.route("/")
def main():
   return render_template('index.html')

@app.route("/api/v1/users/",methods=["GET"])
def get_items():

    response = table.scan()
    for item in response['Items']:
        item.pop('password',None)
    return jsonify(response['Items'])
        





@app.route("/searchSubmit", methods = ["POST"])
def search():
        details = request.form
        print(details)
        numAdults = details['numAdults']
        numChildren = details['numChildren']
        numInfants = details['numInfants']
        location = details['location']
        checkinDate = details['checkindate']
        checkoutDate = details['checkoutdate']
        
        searchTable.put_item(
                Item = {
                        'searchid':str(uuid.uuid4()),
                        'numAdults':numAdults,
                        'location':location,
                        'checkindate':checkinDate,
                        'numChildren':numChildren,
                        'numInfants':numInfants,
                        'checkoutDate':checkoutDate
                }
        )
        
        lookupMap = {}
        lookupMap['tokyo'] = '/static/images/tokyo.jpg'
        lookupMap['lachen'] = '/static/images/village.jpg'
        lookupMap['himalayas'] = '/static/images/himalayas.jpeg'
        lookupMap['pondi'] = '/static/images/cabin2.jpg'
        if(location not in lookupMap):
                return render_template('index.html')
        return lookupMap[location]

@app.route('/showSignUp',methods=['GET', 'POST'])
def showSignUp():
    if request.method == "POST":
        details = request.form
        usernam = details['uname']
        firstName = details['fname']
        lastName = details['lname']
        email    =details['email']
        password =details['password']
        table.put_item(
        Item={
        'username':usernam,
        'first_name':firstName,
        'last_name':lastName,
        'email':email,
        'password':pwd_context.encrypt(password)

             }
                        )


#SES Email trigger

        RECIPIENT= email

        response = client.send_email(
            Destination={
                'ToAddresses': [
                      RECIPIENT,

                               ],


                         },
            Message={

                'Body': {

                    'Html': {

                          'Charset': CHARSET,

                           'Data': BODY_HTML,

                    },


                    'Text': {

                        'Charset': CHARSET,

                        'Data': BODY_TEXT,



                    },

               },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,

                                    )












        return 'Please check email for signup confirmation'
    return render_template('signup.html')

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)
