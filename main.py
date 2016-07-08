#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):

        return self.render_template("main.html")

    def post(self):

        kilometers = float(self.request.get("input_number"))
        kilograms = float(self.request.get("input_number_2"))
        centimeters = float(self.request.get("input_number_3"))

        def convert_to_miles(kilometers):
            miles = kilometers * 0.621371192
            return round(miles, 4)

        def convert_to_pounds(kilograms):
            pounds = kilograms * 2.204622
            return round(pounds, 4)

        def convert_to_inches(centimeters):
            inches = centimeters / 2.54
            return round(inches, 4)

        environment = dict()
        environment['convert_to_miles'] = convert_to_miles(kilometers)
        environment['convert_to_pounds'] = convert_to_pounds(kilograms)
        environment['convert_to_inches'] = convert_to_inches(centimeters)

        self.write("Entered was: " + str(kilometers) + " kilometers. " + str(kilograms) + " kilograms. " +
                   str(centimeters) + " meters.")

        return self.render_template("main.html", params=environment)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
