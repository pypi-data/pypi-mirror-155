from bertdotbill.cli import parse_args
from bertdotbill.config import AppConfig
from bertdotbill.defaults import default_footer_websocket_address
from bertdotbill.defaults import default_rightpane_websocket_address
from bertdotbill.entrypoint import get_static_folder
from bertdotbill.logger import Logger
from bertdotbill.topics import Topics
from bertdotbill.lessons import Lessons
from bertdotbill.websocket import WebSocket
from flask import Flask, jsonify, request, render_template, send_from_directory
import os

import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/javascript', '.mjs')
mimetypes.add_type('text/css', '.css')

# Read command-line args
args = parse_args()
# Initialize logging facility
logger_obj = Logger(logfile_path=args.logfile_path, logfile_write_mode=args.logfile_write_mode)
logger = logger_obj.init_logger(__name__)

# Initialize Config Reader
settings = AppConfig().initialize(
  args=vars(args), verify_tls=args.verify_tls
)

static_assets_folder = args.static_assets_folder or get_static_folder()
logger.info(f'Static sssets folder is {static_assets_folder}')

# Initialize Lesson Loader
topics = Topics(
  settings=settings,
  args=args)

# Initialize Lesson Loader
lessons = Lessons(
    settings=settings,
    args=args)

# Initialize Lesson Loader
websocket = WebSocket()

def main():

  app = Flask(__name__, static_url_path='', static_folder=static_assets_folder)

  # Serve React App
  @app.route('/', defaults={'path': ''})
  @app.route('/<path:path>')
  def serve(path=""):
      if path != "" and os.path.exists(app.static_folder + '/' + path):
          return send_from_directory(app.static_folder, path)
      else:
          return send_from_directory(app.static_folder, 'index.html')


  @app.route('/api/sendToWebsocket', methods=['POST'])
  def send_to_websocket():
      try:
        wsURL = request.json.get('wsURL')
        data = request.json.get('data')
        websocket.send_to_websocket(wsURL, data)
        resp = jsonify(success=True)
      except Exception as e:
        resp = jsonify(error=True)
      return resp

  @app.route('/api/loadLesson', methods=['POST'])
  def load_lesson():
      lesson_uri = request.json.get('uri')
      encoded_lesson_obj = lessons.load_lesson(lesson_uri)
      return encoded_lesson_obj

  @app.route('/api/getRightPaneWebSocketAddress')
  def get_rightpane_websocket_address():
      default_address = settings.get('terminals.rightpane.address', default_rightpane_websocket_address)
      effective_address = default_address
      response_obj = {'address': effective_address}
      return response_obj

  @app.route('/api/getFooterWebSocketAddress')
  def get_footer_websocket_address():
      default_address = settings.get('terminals.footer.address', default_footer_websocket_address)
      effective_address = default_address
      response_obj = {'address': effective_address}
      return response_obj

  @app.route('/api/getTopics')
  def get_topics():
      available_topics = topics.get()
      return available_topics

  @app.route('/api/ping')
  def get_current_time():
      return {'message': "pong"}

  app.run(use_reloader=True, host='0.0.0.0')

if __name__ == '__main__':
  main()