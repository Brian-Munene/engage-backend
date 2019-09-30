from flask import Flask
import cherrypy

from routes import app, db


cherrypy.tree.graft(app.wsgi_app, '/')
cherrypy.config.update({'server.socket_host': '127.0.0.1',
                           'server.socket_port': 5000,
                           'engine.autoreload.on': False,
                        })
if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'employee-engagement'
    app.config['GOOGLE_CLIENT_ID'] = '218366592776-q0aub0931ioo8kpg3802v6ual059m9pn.apps.googleusercontent.com'
    app.config['GOOGLE_CLIENT_SECRET'] = 'RwiF4L6qG_wjLjuU7Pss4pqq'
    try:
        cherrypy.engine.start()
    except KeyboardInterrupt:
        cherrypy.log("Blah", traceback=True)
        cherrypy.engine.stop()

    # Mount the application
    # cherrypy.tree.graft(app, "/")

    # Unsubscribe from the default server
    # cherrypy.server.unsubscribe()

    # Instantiate a new server object
    # server = cherrypy._cpserver.Server()

    # Configure the server object
    # server.socket_host = "0.0.0.0"
    # server.socket_port = 5000
    # server.thread_pool = 30

    # For SSL Support
    # server.ssl_module            = 'pyopenssl'
    # server.ssl_certificate       = 'ssl/certificate.crt'
    # server.ssl_private_key       = 'ssl/private.key'
    # server.ssl_certificate_chain = 'ssl/bundle.crt'

    # server.ssl_module = 'builtin'
    # server.ssl_certificate = '/config/fullchain2.pem'
    # server.ssl_private_key = '/config/privkey2.pem'

    # Subscribe this server
    # server.subscribe()

    # Start the server engine (Option 1 *and* 2)

    # cherrypy.engine.start()
    # cherrypy.engine.block()

    # app.run(debug=True, port=7001)
