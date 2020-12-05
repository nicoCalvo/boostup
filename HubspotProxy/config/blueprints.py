from landing.home import home_page


def register_blueprints(app):
    app.register_blueprint(home_page)

