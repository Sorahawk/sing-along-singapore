from story import *
from feedback import *
from upload import *
import os
import jinja2
import webapp2
import csv
import string
import operator

from random import choice
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


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


# ----------------------------------------------------------------------------------------------------------------------
# When I attempted to create seperate python files for the below code, the error was "No module named ______" which
# strangely does not happen with the feedback.py, story.py and upload.py files


def songlistfunc():

    length = 0
    list_years = []
    list_titles = []
    list_tags = []
    list_sources = []

    with open("songs_list.csv", 'r') as infile:
        records = csv.reader(infile, delimiter=",")

        for record in records:
            list_years.append(record[0])
            list_titles.append(record[1])
            list_tags.append(record[2])
            list_sources.append(record[3])
            length += 1

    return [length, list_years, list_titles, list_tags, list_sources]


def six_random_int():

    list = songlistfunc()
    length = list[0]
    number_line = []
    for num in range(length):
        number_line.append(num)

    chosen_ints = []
    i = 0
    while i < 6:
        a = choice(number_line)
        chosen_ints.append(a)
        number_line.remove(a)
        i += 1

    chosen_ints = sorted(chosen_ints)
    return chosen_ints


def specificsongs(tags):
    songs_list = songlistfunc()

    length = songs_list[0]
    song_years = songs_list[1]
    song_titles = songs_list[2]
    song_tags = songs_list[3]
    song_sources = songs_list[4]

    tags = tags.split()
    list = []

    for num in range(length):
        for tag in tags:
            if song_tags[num].lower() == tag.lower():
                list.append(num)

    return [list, song_years, song_titles, song_sources]


class SongPage(webapp2.RequestHandler):

    def get(self):

        num = int(self.request.get('num'))

        song_list = songlistfunc()
        year = song_list[1][num]
        title = song_list[2][num]
        source = song_list[4][num]

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'num': num,
            'year': year,
            'title': title,
            'source': source,
            'url': url,
            'url_linktext': url_linktext,
            }

        template = JINJA_ENVIRONMENT.get_template('song_page.html')
        self.response.write(template.render(template_values))


class Featured(webapp2.RequestHandler):

    def get(self):

        song_list = songlistfunc()
        length = song_list[0]
        list_years = song_list[1]
        list_titles = song_list[2]
        list_sources = song_list[4]

        ints = six_random_int()

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'length': length,
            'list_years': list_years,
            'list_sources': list_sources,
            'list_titles': list_titles,
            'ints': ints,
            'url': url,
            'url_linktext': url_linktext,
            }

        template = JINJA_ENVIRONMENT.get_template('featured.html')
        self.response.write(template.render(template_values))


class Search(webapp2.RequestHandler):
    def get(self):
        songs_list = songlistfunc()
        search = self.request.get('search')
        search = str(search)
        exclude = set(string.punctuation)
        search = ''.join(ch for ch in search if ch not in exclude)

        search = search.split()
        length = songs_list[0]
        years = songs_list[1]
        titles = songs_list[2]
        sources = songs_list[4]

        target = []

        for num in range(length):
            x = titles[num]
            x = ''.join(ch for ch in x if ch not in exclude)
            x = x.split()

            for word in x:
                for searchword in search:
                    if word.lower() == searchword.lower():
                        target.append(num)

        x = set(target)
        y = []
        for each in x:
            y.append(each)

        num_occur = []

        while len(target) > 0:
            x = target.count(target[0])
            num_occur.append(x)

            if x > 1:
                for num in range(x):
                    target.remove(target[0])

            elif x == 1:
                target.remove(target[0])

        num_num_of_occur = {}
        for num in range(len(y)):
            num_num_of_occur[y[num]] = num_occur[num]

        occur = sorted(num_num_of_occur.items(), key=operator.itemgetter(1))
        occur = occur[::-1]

        songs = []
        for item in occur:
            songs.append(item[0])

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
            'songs': songs,
            'years': years,
            'titles': titles,
            'sources': sources,
            }

        template = JINJA_ENVIRONMENT.get_template('searchpage.html')
        self.response.write(template.render(template_values))


class National1(webapp2.RequestHandler):
    def get(self):
        list = specificsongs("national")
        specific = list[0][:6]
        years = list[1]
        titles = list[2]
        sources = list[3]
        page_name = "National Day Songs"
        next = True
        next_page = "/national2"

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'specific': specific,
            'years': years,
            'titles': titles,
            'sources': sources,
            'url': url,
            'url_linktext': url_linktext,
            'page_name': page_name,
            'next': next,
            'next_page': next_page,
            }

        template = JINJA_ENVIRONMENT.get_template('stream.html')
        self.response.write(template.render(template_values))


class National2(webapp2.RequestHandler):
    def get(self):
        list = specificsongs("national")
        specific = list[0][6:]
        years = list[1]
        titles = list[2]
        sources = list[3]
        page_name = "National Day Songs"
        back = True
        back_page = "/national"

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'specific': specific,
            'years': years,
            'titles': titles,
            'sources': sources,
            'url': url,
            'url_linktext': url_linktext,
            'page_name': page_name,
            'back': back,
            'back_page': back_page,
            }

        template = JINJA_ENVIRONMENT.get_template('stream.html')
        self.response.write(template.render(template_values))


class SG50(webapp2.RequestHandler):
    def get(self):
        list = specificsongs("sg50")
        specific = list[0]
        years = list[1]
        titles = list[2]
        sources = list[3]
        page_name = "SG50 2015 Songs"

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'specific': specific,
            'years': years,
            'titles': titles,
            'sources': sources,
            'url': url,
            'url_linktext': url_linktext,
            'page_name': page_name,
            }

        template = JINJA_ENVIRONMENT.get_template('stream.html')
        self.response.write(template.render(template_values))


class English(webapp2.RequestHandler):
    def get(self):
        list = specificsongs("english sg50 national")
        specific = list[0][:6]
        years = list[1]
        titles = list[2]
        sources = list[3]
        page_name = "English Songs"
        next = True
        next_page = "/english2"

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'specific': specific,
            'years': years,
            'titles': titles,
            'sources': sources,
            'url': url,
            'url_linktext': url_linktext,
            'page_name': page_name,
            'next': next,
            'next_page': next_page,
            }

        template = JINJA_ENVIRONMENT.get_template('stream.html')
        self.response.write(template.render(template_values))


class English2(webapp2.RequestHandler):
    def get(self):
        list = specificsongs("english sg50 national")
        specific = list[0][6:12]
        years = list[1]
        titles = list[2]
        sources = list[3]
        page_name = "English Songs"
        next = True
        next_page = "/english3"
        back = True
        back_page = "/english1"

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'specific': specific,
            'years': years,
            'titles': titles,
            'sources': sources,
            'url': url,
            'url_linktext': url_linktext,
            'page_name': page_name,
            'next': next,
            'next_page': next_page,
            'back': back,
            'back_page': back_page,
            }

        template = JINJA_ENVIRONMENT.get_template('stream.html')
        self.response.write(template.render(template_values))


class English3(webapp2.RequestHandler):
    def get(self):
        list = specificsongs("english sg50 national")
        specific = list[0][12:]
        years = list[1]
        titles = list[2]
        sources = list[3]
        page_name = "English Songs"
        back = True
        back_page = "/english2"

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'specific': specific,
            'years': years,
            'titles': titles,
            'sources': sources,
            'url': url,
            'url_linktext': url_linktext,
            'page_name': page_name,
            'back': back,
            'back_page': back_page,
            }

        template = JINJA_ENVIRONMENT.get_template('stream.html')
        self.response.write(template.render(template_values))


class Chinese(webapp2.RequestHandler):
    def get(self):
        list = specificsongs("chinese")
        specific = list[0]
        years = list[1]
        titles = list[2]
        sources = list[3]
        page_name = "Chinese Songs"

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'specific': specific,
            'years': years,
            'titles': titles,
            'sources': sources,
            'url': url,
            'url_linktext': url_linktext,
            'page_name': page_name,
            }

        template = JINJA_ENVIRONMENT.get_template('stream.html')
        self.response.write(template.render(template_values))


class Malay(webapp2.RequestHandler):
    def get(self):
        list = specificsongs("malay")
        specific = list[0]
        years = list[1]
        titles = list[2]
        sources = list[3]
        page_name = "Malay Songs"

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'specific': specific,
            'years': years,
            'titles': titles,
            'sources': sources,
            'url': url,
            'url_linktext': url_linktext,
            'page_name': page_name,
            }

        template = JINJA_ENVIRONMENT.get_template('stream.html')
        self.response.write(template.render(template_values))


class Tamil(webapp2.RequestHandler):
    def get(self):
        list = specificsongs("tamil")
        specific = list[0]
        years = list[1]
        titles = list[2]
        sources = list[3]
        page_name = "Tamil Songs"

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.url)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'specific': specific,
            'years': years,
            'titles': titles,
            'sources': sources,
            'url': url,
            'url_linktext': url_linktext,
            'page_name': page_name,
            }

        template = JINJA_ENVIRONMENT.get_template('stream.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
                                          ('/', HomePage),
                                          ('/about', About),
                                          ('/stories', Stories),
                                          ('/enter_story', EnterStory),
                                          ('/delete_story', DeleteStory),
                                          ('/feedback', Feedback),
                                          ('/enter_comment', EnterComment),
                                          ('/delete_comment', DeleteComment),
                                          ('/featured', Featured),
                                          ('/song_page', SongPage),
                                          ('/search', Search),
                                          ('/national', National1),
                                          ('/national2', National2),
                                          ('/sg50', SG50),
                                          ('/english', English),
                                          ('/english2', English2),
                                          ('/english3', English3),
                                          ('/chinese', Chinese),
                                          ('/malay', Malay),
                                          ('/tamil', Tamil),
                                          ('/uploadedvids', UploadedStream),
                                          ('/submit_video', SubmitVideo),
                                          ('/delete_video', DeleteVideo),
                                          ], debug=True)
