import argparse
from bertdotbill.defaults import app_name

def parse_args(**kwargs):

  parser = argparse.ArgumentParser(description=app_name)
  parser.add_argument('--username', '-u', help="Username, if the URL requires authentication")
  parser.add_argument('--password', '-p', help="Password, if the URL requires authentication")
  parser.add_argument('--lesson-url', '-url', help="The URL for the lesson definition")
  parser.add_argument('--static-assets-folder', '-S', help="Explicity specify the folder for static HTML assets")
  parser.add_argument('--config-file', '-f', help="Path to app configuration file")
  parser.add_argument('--logfile-path', '-l', help="Path to logfile")
  parser.add_argument('--logfile-write-mode', '-w', default='w', choices=['a', 'w'], help="File mode when writing to log file, 'a' to append, 'w' to overwrite")
  parser.add_argument('--config-file-templatized', '-fT', action='store_true', default=True, help="Render configuration via jinja2 templating")
  parser.add_argument('--no-ui', '-noui', action='store_true', help="Don't launch the UI")
  parser.add_argument('--debug', action='store_true')
  parser.add_argument('--verify-tls', action='store_true', help='Verify SSL cert when downloading web content', default=False)
  parser.add_argument('--norender-markdown', '-nomarkdown', action='store_true')
  parser.add_argument('run', nargs="?", default=None)
  return parser.parse_args()