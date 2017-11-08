from handlers.base import BaseHandler


class SPAHandler(BaseHandler):

    def get(self):
        self.render_template("spa.html")
