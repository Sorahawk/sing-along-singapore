import os
import jinja2
import webapp2
from urlparse import urlparse
from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Author(ndb.Model):
    identity = ndb.StringProperty()
    email = ndb.StringProperty()


class Video(ndb.Model):
    author = ndb.StructuredProperty(Author)
    title = ndb.StringProperty()
    content = ndb.StringProperty()
    youtube_link = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class UploadedStream(webapp2.RequestHandler):

    def get(self):

        videos_query = Video.query().order(-Video.date)
        videos = videos_query.fetch()

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'videos': videos,
            'url': url,
            'url_linktext': url_linktext,
            }

        template = JINJA_ENVIRONMENT.get_template('videos.html')
        self.response.write(template.render(template_values))


class SubmitVideo(webapp2.RequestHandler):

    def post(self):

        video = Video()

        if users.get_current_user():
            video.author = Author(
                identity=users.get_current_user().user_id(),
                email=users.get_current_user().email())

        video.title = self.request.get('title')
        video.content = self.request.get('content')
        video.youtube_link = urlparse(self.request.get('youtube_link')).query
        video.youtube_link = video.youtube_link[2:]
        video.put()

        self.redirect('/uploadedvids')


class DeleteVideo(webapp2.RequestHandler):

    def post(self):

        video = Video()
        video = video.get_by_id(long(self.request.get('id')))
        video.key.delete()
        self.redirect("/uploadedvids")
