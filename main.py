import webapp2
import jinja2
import os

from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('html_file/home.html')
        self.response.write(template.render())

def address(course):
    courseCode = course['name'].lower()
    name = course['teacher'][0].lower() + course['teacher'][1:]
    return courseCode + "." + name

dictOfTeachers = { "ENGL1A" : {
    'name': "ENGL1A",
    'teacher': "Hendel",
    'class': "English 1A",
    'teaching_style': "60% lecture time with videos in between concepts",
    'homework': "Assigned reading",
},
"CHEM30A" : {
    'name': "CHEM30A",
    'teacher': "Scientist",
    'class': "Chemistry 30A",
},
"AMS1A" : {
    'name': "AMS1A",
    'teacher': "Rycenga",
    'class': "American Studies 1A",
    'full_name': "Jennifer Rycenga",
},
}

classData  = dictOfTeachers.values()          #get values in dictionary


class SearchHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('html_file/searchTeacher.html')
        teacher_list = set()
        for row in Testimonial.query().fetch():
            teacher_list.add(row.teacher)
            #a = filter(lambda x: x['teacher'] == row, classData)
            #map(lambda x: x['teacher'], a)
        teacher_dict = {'teacher_set': teacher_list}
        self.response.write(template.render(teacher_dict))


class Testimonial(ndb.Model):
  teacher = ndb.StringProperty(required=True)
  className = ndb.StringProperty(required=True)
  comment = ndb.StringProperty(required=True, default = False)

class TeacherHandler(webapp2.RequestHandler):
    def assign_teacher(self):
        self.teacherDict = {}
        self.teacher = ""
        self.className = ""
        self.homework = ""

    def get(self):
        self.assign_teacher()
        testimonial_list = []
        for row in Testimonial.query().filter(Testimonial.teacher == self.teacher).fetch():
            testimonial_list.append(row.comment)
        self.teacherDict.update({'appended_list': testimonial_list})
        template = jinja_env.get_template('html_file/teacher.html')
        self.response.write(template.render(self.teacherDict))

    def post(self):
        self.assign_teacher()
        template = jinja_env.get_template('html_file/teacher.html')

        student_input = self.request.get('inputT')
        professor = Testimonial(teacher=self.teacher,
                                                className=self.className ,
                                                comment=student_input)
        # ^ instantiate & add user input to object
        professor.put() #store object in db

        testimonial_list = [] #create list
        for row in Testimonial.query().filter(Testimonial.teacher == self.teacher).fetch():
            testimonial_list.append(row.comment) #add new testimonial to build list
        self.teacherDict.update({'appended_list': testimonial_list}) #put list in global dict
        self.response.write(template.render(self.teacherDict))


class Engl1aHendel(TeacherHandler): #create object
    def assign_teacher(self):
        self.teacherDict = dictOfTeachers['ENGL1A'] #fill in var w/ English dict
        self.teacher = self.teacherDict['teacher']
        self.className = self.teacherDict['class']
        self.homework = self.teacherDict['homework']

class Chem30a(TeacherHandler):
    def assign_teacher(self):
        self.teacherDict = dictOfTeachers['CHEM30A']
        self.teacher = self.teacherDict['teacher']
        self.className = self.teacherDict['class']

class Ams1aRycenga(TeacherHandler):
    def assign_teacher(self):
        self.teacherDict = dictOfTeachers['AMS1A']
        self.teacher = self.teacherDict['teacher']
        self.className = self.teacherDict['class']

class Ams1aRycenga(TeacherHandler):
    def assign_teacher(self):
        self.teacherDict = dictOfTeachers['AMS1A']
        self.teacher = self.teacherDict['teacher']
        self.className = self.teacherDict['class']

class Ams1aRycenga(TeacherHandler):
    def assign_teacher(self):
        self.teacherDict = dictOfTeachers['AMS1A']
        self.teacher = self.teacherDict['teacher']
        self.className = self.teacherDict['class']

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/search.teacher', SearchHandler),
    ('/' + address(dictOfTeachers['ENGL1A']), Engl1aHendel),
    ('/' + address(dictOfTeachers['CHEM30A']), Chem30a),
    ('/' + address(dictOfTeachers['AMS1A']), Ams1aRycenga),
], debug=True)
