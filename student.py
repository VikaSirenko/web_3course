class Student(object):
    _id=""
    userName=""
    firstName=""
    lastName=""


    def __init__(self, _id, userName, firstName, lastName):
        self._id=_id
        self.userName=userName
        self.firstName=firstName
        self.lastName=lastName