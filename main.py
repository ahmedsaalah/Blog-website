"""
that's my module and my name is serag
"""
import webapp2


def sub_m(name, nickname):
    """
    hoho
    """
    given_string2 = """I'm %(nickname)s. My real name is %(name)s,
     but my friends call me %(nickname)s."""
    return given_string2 % {'nickname': nickname, 'name': name}


class MainPage(webapp2.RequestHandler):
    """
    this class handels the main req
    """

    def get(self):
        """
        handle get req

        """
        form = """
        
        <form action="/testform" method="post">
            <input name="name" placeholder="name">
            <input name="nickname" placeholder="nicknameeee">
            <!--input type="checkbox" name="check">
            <input type="radio" name="s" value="serag">
            <input type="radio" name="s">
            <input type="radio" name="s" -->
            <input type="submit">
        </form>
        """
        self.response.headers['Content-Type'] = 'text/HTML'
        self.response.out.write(form)


class TestHandler(webapp2.RequestHandler):
    """
    handel submit format
    """

    def post(self):
        """
        handle get req
        """
        self.response.headers['Content-Type'] = 'text/HTML'
        # name = self.request.get('name')
        # nickname = self.request.get('nickname')
        self.redirect('/thanks')


class ThanksHandler(webapp2.RequestHandler):
    """
    handel thanks
    """

    def get(self):
        """
        handle get req
        """

        nickname = self.request.get('name')
        self.response.out.write(nickname)

        self.response.out.write('Thanks Bro!!')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/testform', TestHandler),
    ('/thanks', ThanksHandler)
], debug=True)
