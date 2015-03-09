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


class Story(ndb.Model):
    author = ndb.StructuredProperty(Author)
    title = ndb.StringProperty()
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class Comment(ndb.Model):
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class HomePage(webapp2.RequestHandler):

    def get(self):

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class About(webapp2.RequestHandler):

    def get(self):

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.write(template.render(template_values))


class Stories(webapp2.RequestHandler):

    def get(self):

        stories_query = Story.query().order(-Story.date)
        stories = stories_query.fetch()

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'stories': stories,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('stories.html')
        self.response.write(template.render(template_values))


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


class EnterStory(webapp2.RequestHandler):

    def post(self):

        story = Story()

        if users.get_current_user():
            story.author = Author(
                identity=users.get_current_user().user_id(),
                email=users.get_current_user().email())

        story.title = self.request.get('title')
        story.content = self.request.get('content')
        story.put()

        self.redirect('/stories')


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

application = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/about', About),
    ('/stories', Stories),
    ('/feedback', Feedback),
    ('/enter_story', EnterStory),
    ('/enter_comment', EnterComment),
], debug=True)
