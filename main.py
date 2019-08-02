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

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('html_file/login.html')
        self.response.write(template.render())

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('html_file/about.html')
        self.response.write(template.render())

class CreateHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('html_file/login2.html')
        self.response.write(template.render())

dictOfTeachers = { "ENGL1A" : {
    'name': "ENGL1A",
    'teacher': "Hendel",
    'class': "English 1A",
    'teaching_style1': "Name: Daniel Hendel De La O",
    'teaching_style2': "Engish 1A is an introductory writing course that will help you understand the writing process and the goals, dynamics, and genres of written communication. through interpretation and analysis of texts, you will learn to think clearly and write effectively as you give form and coherence to complex ideas.",
    'teaching_style3': "Materials:",
    'teaching_style4': "All books are available in an electronic edition (e.g. kindle, nook), though pagination may vary from print editions.",
    'teaching_style5': "Expectations:",
    'teaching_style6': "The class based on a theme given to you in beginning of the semest which you will then think and write reothocally about.",
    'teaching_style7': "Homework:",
    'teaching_style8': "Assigned reading",
    'teaching_style9': "Student Comments:",
    'teaching_style0': "60% lecture time with videos in between concepts",

},
"CHEM30A" : {
    'name': "CHEM30A",
    'teacher': "Franks",
    'class': "Chemistry 30A",
    'teaching_style1': "",
    'teaching_style2': "",
},
"AMS1A" : {
    'name': "AMS1A",
    'teacher': "Rycenga",
    'class': "American Studies 1A",
    'full_name': "Jennifer Rycenga",
    'teaching_style1': "Name: Jennifer Rycenga",
    'teaching_style2': "American studies concludes of political, literary, artistic, economic and social development. American values, ideas and institutions from popular culture as well as traditional sources.",
    'teaching_style3': "Materials:",
    'teaching_style4': "All books are available in an electronic edition (e.g. kindle, nook), though pagination may vary from print editions",
    'teaching_style5': "Student Comments:",
    'teaching_style6': "Her exams are straightforward; they are essay format. ",
    'teaching_style7': "Take good notes because she goes fast on lecture slides. Laptop taking notes are acceptable. Reading is not heavy all.",
    'teaching_style8': "Student Comments:"

},
"MATH30" : {
    'name': "MATH30",
    'teacher': "Obaid",
    'class': "MATH30",
    'teaching_style1': "Name: Samih Obaid",
    'teaching_style2' :"Calculus I class that requires a Workshop, this class consists of the fundamentals of limits, continuous functions, derivatives, fundamental theorem of calculus, integrals, ",
    'teaching_style3': "The teacher provides review packet that is similar to the test, many students find this very helpful. ",
    'teaching_style4': "Materials:",
    'teaching_style5': "Textbooks and notebooks",
    'teaching_style6': "NO COMPUTERS NEEDED OR ANY ELECTRONICS DEVICES",
    'teaching_style7': "Student Comments:",
    'teaching_style8': "Lectures with hundreds of students.",
    'teaching_style9': "The teacher teaches at a good speed that allows the students to fully understand the concepts.",

},
}

classData  = dictOfTeachers.values()          #get values in dictionary


class SearchHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('html_file/searchTeacher.html')
        #teacher_list = set()
        #for row in Testimonial.query().fetch():
            #teacher_list.add(row.teacher)
            #a = filter(lambda x: x['teacher'] == row, classData)
            #map(lambda x: x['teacher'], a)
        teachers = {'classData': classData}
        self.response.write(template.render(teachers))


class Testimonial(ndb.Model):
  teacher = ndb.StringProperty(required=True)
  className = ndb.StringProperty(required=True)
  comment = ndb.StringProperty(required=True, default = False)

class TeacherHandler(webapp2.RequestHandler):
    def assign_teacher(self):
        self.teacherDict = {}
        self.teacher = ""
        self.className = ""
        #self.homework = ""

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

class Math30Obdaid(TeacherHandler):
    def assign_teacher(self):
        self.teacherDict = dictOfTeachers['MATH30']
        self.teacher = self.teacherDict['teacher']
        self.className = self.teacherDict['class']


app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/search.teacher', SearchHandler),
    ('/' + address(dictOfTeachers['ENGL1A']), Engl1aHendel),
    ('/' + address(dictOfTeachers['CHEM30A']), Chem30a),
    ('/' + address(dictOfTeachers['AMS1A']), Ams1aRycenga),
    ('/' + address(dictOfTeachers['MATH30']), Math30Obdaid),
    ('/login', LoginHandler),
    ('/about', AboutHandler),
    ('/login2', CreateHandler),
], debug=True)
