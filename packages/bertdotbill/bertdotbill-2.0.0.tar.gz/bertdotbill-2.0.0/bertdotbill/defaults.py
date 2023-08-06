# Set App Name
app_name = "Bert's Interactive Lesson Loader (BILL)"
gui_dirname = 'bill.gui'
default_websocket_address = 'ws://127.0.0.1:5000/ws'
default_footer_websocket_address = default_websocket_address
default_rightpane_websocket_address = default_websocket_address
default_config_file_name = 'bill.config.yaml'

settings = {
  "terminals": {
    "default": {
      "address": default_websocket_address
    },
    "footer": {
      "address": default_footer_websocket_address
    },
    "rightpane": {
      "address": default_rightpane_websocket_address
    }
  },
  "external_configs": [
    {
      "name": "bertdotlessons",
      "uri": "https://raw.githubusercontent.com/berttejeda/bert.lessons/main/bill.config.yaml"
    }
  ]
}