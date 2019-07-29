import webapp2
import jinja2
import os

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# the handler section
class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('html_file/home.html')
        self.response.write(template.render())

class TeacherHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('html_file/teacher.html')
        ENGL1A = {
            'teacher': "Professor",
            'class': "English 1A",
        }
        self.response.write(template.render(ENGL1A))
    def post(self):  # for a get request
        template = jinja_env.get_template('html_file/teacher.html')
        student_input = self.request.get('input')
        ENGL1A = {
            'testimonial': student_input,
        }
        self.response.write(template.render(ENGL1A))




app = webapp2.WSGIApplication([
    ('/', TeacherHandler),
    ('/teacher', TeacherHandler),
], debug=True)
