import logging


def handle_404(request, response, exception):
    logging.error(exception)
    response.write("Sorry, the princess is in another castle!")
    response.set_status(404)


def handle_500(request, response, exception):
    logging.error(exception)
    response.write("Server error.")
    response.set_status(500)
