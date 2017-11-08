import webapp2

import routes

from appengine_config import APP_CONFIG
from appengine_config import DEBUG_MODE_ENABLED
from handlers import errors as error_handlers

# Define app
app = webapp2.WSGIApplication(config=APP_CONFIG, debug=DEBUG_MODE_ENABLED)

# Add defined routes
routes.add_routes(app)

# Define error handlers
app.error_handlers[404] = error_handlers.handle_404
app.error_handlers[500] = error_handlers.handle_500
