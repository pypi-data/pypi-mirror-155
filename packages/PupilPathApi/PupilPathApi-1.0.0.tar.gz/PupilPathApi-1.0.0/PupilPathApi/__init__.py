from bs4 import BeautifulSoup

import requests

session = requests.Session()

class User:
    
    def __init__(self, dataDictonary):
        assert type(dataDictonary) == dict, "Expected dictonary got " + str(type(dataDictonary))

        session.get("https://pupilpath.skedula.com/beginSession.aspx")

        payload = {
            "user[username]" : dataDictonary["Username"],
            "user[password]" : dataDictonary["Password"]
        }
        
        loginPost = session.post(url = "https://auth.ioeducation.com/users/sign_in", data = payload)

        if len(loginPost.text) < 5000:
            raise Exception("Some of your credentials are incorrect")

        loginPostParsed = BeautifulSoup(loginPost.text, "html.parser").find("option")

        studentDataPost = session.post(
            url = "https://pupilpath.skedula.com/auth/login/getStudents.aspx?ajax=true",

            data = {
                "DBN": loginPostParsed["value"],
                "Term": loginPostParsed["data-term"]
            }
        )

        studentDataParsed = BeautifulSoup(studentDataPost.text, "html.parser").find("option")

        payload = {
            "DBN": loginPostParsed["value"],
            "Term": loginPostParsed["data-term"],
            "Student": studentDataParsed["value"],
            "StudentName": studentDataParsed["data-studentname"]
        }

        mainPage = session.post(url = "https://pupilpath.skedula.com/auth/login/loginPupilPath.aspx", data = payload)

        self.StudentName = studentDataParsed["data-studentname"]
        self.ClassCount = len(BeautifulSoup(mainPage.text, "html.parser").find("tbody"))

        self.Session = session
    
    def GetClassData(self):
        studentData = {"Title": [], "Teacher": [], "Department": [], "Average": []}

        dashboard = BeautifulSoup(
            self.Session.get(url = "https://pupilpath.skedula.com/home/dashboard/").text, "html.parser"
        )

        stuff = {"Title" : [1, 5], "Teacher" : [2, 5], "Department" : [3, 5], "Average" : [4, 5]}
        
        for titleGoal in stuff:

            for element in dashboard.find_all("td")[stuff[titleGoal][0] :: stuff[titleGoal][1]]:
                elementText = element.text

                studentData[titleGoal].append(
                    elementText.split(": ")[1].strip() if not elementText.find("MP") else elementText.strip()
                )

        return studentData

    def GetGradeData(self):
        gradesList = []

        for average in self.GetClassData()["Average"]:
            try:
                gradesList.append(float(average))
            except:
                pass

        studentAverage = sum(gradesList) / len(gradesList)

        def getOverallGrade(grade):
            gradesMapping = {0: "Failing", 60: "Borderline", 80: "Average", 90: "Honors"} 

            for mappedGrade in gradesMapping.keys():
                if mappedGrade <= grade:
                    key = mappedGrade
            
            return gradesMapping[key]
    
        return {"Average" : studentAverage, "Overall" : getOverallGrade(studentAverage)}

    def SendEmail(self, recipients, contentDict):
        assert type(recipients) == list, "Expected a list of recipients got " + str(type(recipients))
        assert type(contentDict) == dict,"Expected dictonary for content got" + str(type(contentDict))

        payload = {
            "action" : "send",
            "recipients" : (", ").join(recipients),
            "subject" : contentDict["Subject"],
            "text" : "<p>" + contentDict["Content"] + "</p>",
        }

        session.post(url = "https://pupilpath.skedula.com/Mail/ajax.aspx", data = payload)