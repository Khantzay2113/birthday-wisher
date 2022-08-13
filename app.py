import time
from flask import Flask,render_template ,request
from email.message import EmailMessage
import csv
import random
import smtplib
import ssl

count = 13

def addmails(receiver_names,emails,dates,months):         
        user_data = {}

        user_data['Sender'] = now_username
        user_data['Receiver'] = receiver_names
        user_data["Email"] =  emails
        user_data['Date'] = dates
        user_data["Month"] = months

        fieldnames = []
        for key in user_data:
            fieldnames.append(key)

        with open(f"data/user_data/{now_username}.txt", "a") as data_file:
            writer = csv.DictWriter(data_file, fieldnames)
            writer.writerow(user_data)

def check_mail(name,mail,month,date):
    with open(f"data/user_data/{now_username}.txt") as data:
        mail_data = csv.DictReader(data)
        for mails in mail_data:
            if str(mails['Email']) == str(mail):
                print('already add this email')
                return render_template("add.html")
        addmails(name,mail,month,date)
        
def filecheck():#this will check that username and password file will create
        try:
            with open(f"data/user_data/{now_username}.txt",mode='r')as fall:
                pass

        except FileNotFoundError:
            with open(f'data/user_data/{now_username}.txt', 'a') as csvfile:
                global code_for_pass 
                fieldnames = ['Sender','Receiver','Email','Date','Month']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                pass


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/c_username",methods=["POST"])
def c_username():
    global now_username,now_password
    now_username = request.form.get("c_username")
    now_password = request.form.get("c_password")
    print(now_username)
    with open("data/data.txt") as all_data:
        data = csv.DictReader(all_data)
        for userdata in data:
            if userdata["Usernames"] == now_username:
                print(userdata["Passwords"])
                if userdata["Passwords"] == now_password:
                    return render_template('option.html',username=now_username)

@app.route("/option")
def option():
    return render_template("option.html")
            
@app.route("/addmail")
def addmail():
    return render_template("add.html")

@app.route("/add_process",methods=["POST"])
def add_process():
    receiver_name = request.form.get("receiver_name")
    email = request.form.get("email")
    date = request.form.get("date")
    month = request.form.get("month")

    filecheck()
    check_mail(receiver_name,email,date,month)
    return render_template("index.html")

    

def c_and_sendmail():
    from datetime import date
    today = date.today()

    month = today.strftime("%m")
    date = today.strftime("%d")

    with open("data/data.txt", "r") as data_file:
        user_data = csv.DictReader(data_file)
        for user in user_data:
            with open(f"data/user_data/{user['Usernames']}.txt", "r") as data_file:
                user_data = csv.DictReader(data_file)
                for user in user_data:
                    if user['Month'] == month:
                        if user['Date'] == date:
                            username = user['Receiver']
                            sent_mail = user['Email']

                            # Define email sender and receiver
                            email_sender = 'aviothic.pizza@gmail.com'
                            email_password = 'wgbmsdugyaxwtkaz'
                            email_receiver = sent_mail
                            name = username

                            # Set the subject and body of the email
                            with open("data/wish.txt")as letters:
                                orange = letters.read()
                                bb = orange.replace("[name]",name)
                                cc = bb.replace("[Sender]",user['Sender'])
                            subject = 'Birthday Wish'
                            body = cc

                            em = EmailMessage()
                            em['From'] = email_sender
                            em['To'] = email_receiver
                            em['Subject'] = subject
                            em.set_content(body)

                            # Add SSL (layer of security)
                            context = ssl.create_default_context()

                            # Log in and send the email
                            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                smtp.login(email_sender, email_password)
                                smtp.sendmail(email_sender, email_receiver, em.as_string())


if __name__ == "__main__":
    import datetime
    now = datetime.datetime.today()
    if now.day == count:
        print(count)
        print('ok')
        c_and_sendmail()
        count += 1

    print(count)
    app.run(host='0.0.0.0',port=random.randint(2000,9000))