import os
import jinja2
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Author(ndb.Model):
    identity = ndb.StringProperty()
    email = ndb.StringProperty()


class Comment(ndb.Model):
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class Feedback(webapp2.RequestHandler):

    def get(self):

        comments_query = Comment.query().order(-Comment.date)
        comments = comments_query.fetch()

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'comments': comments,
            'url': url,
            'url_linktext': url_linktext,
            }

        template = JINJA_ENVIRONMENT.get_template('feedback.html')
        self.response.write(template.render(template_values))


class EnterComment(webapp2.RequestHandler):

    def post(self):

        comment = Comment()

        if users.get_current_user():
            comment.author = Author(
                identity=users.get_current_user().user_id(),
                email=users.get_current_user().email())

        comment.content = self.request.get('content')
        comment.put()

        self.redirect('/feedback')


class DeleteComment(webapp2.RequestHandler):

    def post(self):

        comment = Comment()
        comment = comment.get_by_id(long(self.request.get('id')))
        comment.key.delete()
        self.redirect("/feedback")
