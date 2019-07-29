import webapp2
import jinja2
import os

from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# the handler section
class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('html_file/home.html')
        self.response.write(template.render())

ENGL1A = {
    'teacher': "Professor",
    'class': "English 1A",
}

class Testimonial(ndb.Model):
  teacher = ndb.StringProperty(required=True)
  classname = ndb.StringProperty(required=True)
  message = ndb.StringProperty(required=True)

class TeacherHandler(webapp2.RequestHandler):

    def get(self):
        testimonial_list = []
        for count in Testimonial.query().fetch():
            testimonial_list.append(count.message)
        ENGL1A.update({'message_list': testimonial_list})
        template = jinja_env.get_template('html_file/teacher.html')
        self.response.write(template.render(ENGL1A))

    def post(self):
        template = jinja_env.get_template('html_file/teacher.html')

        student_input = self.request.get('inputT')
        professorENGL = Testimonial(teacher="Professor", classname="English 1A", message=student_input)
        # ^ new object & add user input to object
        professorENGL.put() #store object in db

        testimonial_list = [] #create list
        for count in Testimonial.query().fetch():
            testimonial_list.append(count.message) #add new testimonial to build list
        ENGL1A.update({'new_key': testimonial_list}) #put list in global dict
        self.response.write(template.render(ENGL1A))

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/teacher', TeacherHandler),
], debug=True)
