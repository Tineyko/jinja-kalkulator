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
        if params is None:
        #if not params: --> napacno!
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("kalkulator.html")

    def post(self):
        stevilo1 = self.request.get("stevilo-1")
        stevilo2 = self.request.get("stevilo-2")
        operacija = self.request.get("operand")
        if (stevilo1.isdigit() and stevilo2.isdigit() ):
            rezultat = None
            if (operacija == "+"):
                rezultat = {"vnos": "{0} {1} {2}".format(stevilo1, operacija, stevilo2),"rezultat_racuna": float(stevilo1) + float(stevilo2)}
            if (operacija == "-"):
                rezultat = {"vnos": "{0} {1} {2}".format(stevilo1, operacija, stevilo2),"rezultat_racuna": float(stevilo1) - float(stevilo2)}
            if (operacija == "*"):
                rezultat = {"vnos": "{0} {1} {2}".format(stevilo1, operacija, stevilo2),"rezultat_racuna": float(stevilo1) * float(stevilo2)}
            if (operacija == "/"):
                rezultat = {"vnos": "{0} {1} {2}".format(stevilo1, operacija, stevilo2),"rezultat_racuna": float(stevilo1) / float(stevilo2)}

            return self.render_template("kalkulator.html", params = rezultat)
        else:
            rezultat = {"rezultat_racuna": "Samo stevilke!"}
            return self.render_template("kalkulator.html", params=rezultat)
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
