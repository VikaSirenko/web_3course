import pymongo 
from student import *

client = pymongo.MongoClient("mongodb+srv://VikaSirenko:16842778@cluster0.8kq1ltu.mongodb.net/?retryWrites=true&w=majority")
db = client.kp1
coll=db.students

class StudentRepository:

    def getListOfStudents(self):
        all_students= coll.find()
        string_list = ""
        
        list_students=[]
        for user in all_students:
            _id=user["_id"]
            userName=user["userName"]
            firstName=user["firstName"]
            lastName=user["lastName"]
            student= Student(_id, userName, firstName, lastName)
            list_students.append(student)
        
        return list_students


    def userExist(self,userName):
        query = {"userName": userName}
        student=coll.find_one(query)
        if(student!=None):
            return True
        else:
            return False


    def createStudent(self, student):
        all_students=self.getListOfStudents()
        for user in all_students:
            if(user.userName==student.userName):
                return None
        new_student={"userName": student.userName, "firstName":student.firstName, "lastName":student.lastName}
        result=coll.insert_one(new_student)
        return result.inserted_id


    


