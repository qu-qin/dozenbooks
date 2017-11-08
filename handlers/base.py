import os
import webapp2

from webapp2_extras import jinja2


# Configured so that uri_for can be used in JINJA templates
def jinja2_factory(app):
    j = jinja2.Jinja2(app)
    j.environment.globals.update({
        "uri_for": webapp2.uri_for
    })

    return j


class BaseHandler(webapp2.RequestHandler):

    """
    This class defines a base handler for all the request handlers
    and eases the use of jinja2 templates
    """

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(factory=jinja2_factory)

    @webapp2.cached_property
    def is_dev_mode(self):
        """Return true for dev environment """
        return os.environ.get("SERVER_SOFTWARE", "Development").startswith("Development")

    def render_template(self, filename, **template_args):

        # set or overwrite special vars for jinja templates
        template_args.update({
            "url": self.request.url,
            "path": self.request.path,
            "query_string": self.request.query_string,
            "is_dev_mode": self.is_dev_mode
        })

        self.response.headers.add_header("X-UA-Compatible", "IE=Edge,chrome=1")
        self.response.write(self.jinja2.render_template(filename, **template_args))
