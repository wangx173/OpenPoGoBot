from threading import Thread
import os
import logging
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_socketio import SocketIO, emit

from pokemongo_bot import logger
from pokemongo_bot.event_manager import manager

# pylint: disable=unused-variable, unused-argument

logging.getLogger('socketio').disabled = True
logging.getLogger('engineio').disabled = True
logging.getLogger('werkzeug').disabled = True


def run_flask():
    root_dir = os.path.join(os.getcwd(), 'web')
    app = Flask(__name__, static_folder=root_dir)
    app.use_reloader = False
    app.debug = False
    app.config["SECRET_KEY"] = "OpenPoGoBot"
    socketio = SocketIO(app, logging=False, engineio_logger=False)

    logging_buffer = []

    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    @app.route('/<path:path>')
    def static_proxy(path):
        return app.send_static_file(path)

    @manager.on("logging")
    def logging_event(text="", color="black"):
        line = {"output": text, "color": color}
        logging_buffer.append(line)
        socketio.emit("logging", [line], namespace="/event")

    @socketio.on("connect", namespace="/event")
    def connect():
        socketio.emit("logging", logging_buffer, namespace="/event")
        logger.log("Web client connected", "yellow")

    @socketio.on("disconnect", namespace="/event")
    def disconnect():
        logger.log("Web client disconnected", "yellow")

    socketio.run(app, host="0.0.0.0", port=8000, debug=False, use_reloader=False, log_output=False)


WEB_THREAD = Thread(target=run_flask)
WEB_THREAD.daemon = True
WEB_THREAD.start()
