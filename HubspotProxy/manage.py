# -*- coding: utf-8 -*-

import sys
import urllib.parse

from flask import url_for
from flask_script import (
    Manager,
    Server
)

from app import app


manager = Manager(app)

manager.add_command("runserver",
                    Server(use_debugger=True,
                           use_reloader=True,
                           host='0.0.0.0',
                           port=9999,
                           ssl_context=('certs/cert.pem', 'certs/key.pem')))


@manager.command
def list_routes():
    """
    List all registed blueprints/routes and method associated with it:

    simple_page.show                                   HEAD,GET,OPTIONS     /[page]
    simple_page.show                                   HEAD,GET,OPTIONS     /[page]
    static                                             HEAD,GET,OPTIONS     /static/[filename]

    """

    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


if __name__ == "__main__":
    manager.run()
