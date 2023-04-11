from flask import Flask, request
from bd import *
from student import *
from flask import copy_current_request_context
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY']="thisisthesecretkey"

connection= StudentRepository()
    

@app.route('/getStudents', methods=['GET'])
def getListOfStudents():
    try:
        all_students= connection.getListOfStudents()
        if(len(all_students)!=0):
            string_list = ""
            for user in all_students:
                string_list += user.userName+": "+user.firstName+" "+user.lastName+"\n"
            return string_list, 200
        else:
            return ("There is no student in the database"), 404
    except:
        return "It is impossible to get the list of students", 400



@app.route('/getToken', methods=['GET'])
def getToken():
    try:
        content = request.json
        userName = content['userName']
        exist=connection.userExist(userName)
        if(exist):
            token=jwt.encode({'userName':userName, 'exp': datetime.datetime.utcnow()+ datetime.timedelta(hours=24)}, app.config["SECRET_KEY"])
            return token, 200
        else:
            return ("There is no student with this username"), 404
    except: 
        return "Unable to get token", 400




def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token =request.args.get('token')

        if not token:
            return "Token is missing", 403
        
        
        try:
            data=jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print(data)
            return f(*args, **kwargs), 200
        except:
            return "Token is invalid", 403
    return decorated




@app.route('/createStudent', methods=['POST'])
@token_required
def createStudent():
    try:
        content = request.json
        student= Student(0, content['userName'], content['firstName'], content['lastName'])
        result=connection.createStudent(student)
        #return result, 200
        #if(newId==None):
            #return "Student is not created  ", 404
        #else:
        return "Student created", 200
    except:
        return "It is not possible to create a new student", 404



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")