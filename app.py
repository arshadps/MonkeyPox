from flask import Flask,render_template,request,url_for,redirect,session
from config import Database
import os
app=Flask(__name__)
db=Database()
app.secret_key = 'asd'

@app.route("/")
def home():
    return render_template("guest/index.html ")

#change

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        print("post Sucess")
        username=request.form["username"]
        password=request.form["password"]

        print(username)
        print(password)

        query=f"select * from tbl_login where username='{username}'and password='{password}'"
        print(query)

        user=db.fetchone(query)
        
        if user:
            session['login_id']=user['id']
            if user["user_type"]=="admin":
                print("welocome admin")
                return redirect( url_for("admin"))

            elif user["user_type"]=="user":
                print("welcome user")
                return redirect( url_for("userhome"))

            else:
                print("invalid user")
        else:
            print("login fails")




    return render_template("guest/login.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/userhome")
def userhome():
    return render_template("user/index.html")

@app.route("/userenquiry")
def userenquiry():
    user_id = session['login_id']
    if request.method=="POST":

        
        print("User ID:", user_id)

        file = request.files["storeImage"]
        filename = file.filename
        filepath = os.path.join('./static/enq_images/', filename)
        file.save(filepath)


        fever=request.form['fever']

        headache=request.form['headache']

        muscle=request.form['muscle']

        rashes=request.form['rashes']

        swollen=request.form['swollen']

        exhausion=request.form['exhausion']

        chills=request.form['chills']

        
        details=request.form['details']

        query = f"""
            INSERT INTO tbl_enquiry 
            (user_id, image, fever, headache, muscle, rashes, swollen, exhausion, chills, details, status) 
            VALUES ({user_id}, '{filename}', '{fever}', '{headache}', '{muscle}', '{rashes}', '{swollen}', '{exhausion}', '{chills}', '{details}', 'initiated')
        """
        print(query)
        success = db.single_insert(query)


        if success:
            print("Enquiry submitted successfully.")
            return redirect(url_for("user"))


        else:
            print("Failed to submit enquiry.")




    return render_template("user/enquiry.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=='POST':
        firstname=request.form['Fname']
        print(firstname)

        lasttname=request.form['Lname']
        print(lasttname)

        age=request.form['age']
        print(age)

        phon=request.form['phone']
        print(phon)

        Address=request.form['address']
        print(Address)

        gender=request.form['gender']
        print(gender)

        blood=request.form['blood_group']
        print(blood)

        dia=request.form['diabetic']
        print(dia)

        aller=request.form['allergy']
        print(aller)

        height=request.form['height']
        print(height) 

        weight=request.form['weight']
        print(weight)

        #insert into tbl_login
        #if insert success
            #insert into tbl_user along with login_id

        username = request.form["username"]
        print(username)

        password = request.form["password"]
        print(password)

        ins1=f"INSERT INTO tbl_login(username,password,user_type) values('{username}','{password}','user')"
        login_id=db.executeAndReturnId(ins1)
        if login_id:
            ins2=f"INSERT INTO `tbl_user`(`fname`, `lname`, `gender`,`age`, `phone`, `address`, `blood_group`, `allergy`, `diabetics`, `height`, `weight`, `login_id`)  values ('{firstname}','{lasttname}','{gender}','{age}','{phon}','{Address}','{blood}','{dia}','{aller}','{height}','{weight}','{login_id}')"
            insRes=db.single_insert(ins2)
            print("hello")
            
            print("registration successful")
            return redirect(url_for("login"))

    return render_template("guest/register.html")

if __name__=="__main__":
    app.run(debug=True)