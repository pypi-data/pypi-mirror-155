import hashlib
import hmac
import logging
import socketio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

try:
    import asyncio
except ImportError:
    import trollius as asyncio


class Plugin(socketio.ClientNamespace):

    def __init__(self, plugin_id, api_key, callback):
        super().__init__('/plugin')
        self.plugin_id = plugin_id
        self.api_key = api_key
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.heartbeat, 'interval', seconds=60)
        scheduler.start()
        self.logger = logging.getLogger()
        self.callback = callback

    def on_connect(self):
        self.logger.warning("Connected")
        self.heartbeat()

    def on_disconnect(self):
        self.logger.warning("Disconnected")

    def heartbeat(self):
        self.emit('heartbeat', {"id": self.plugin_id, "secret": self.api_key})

    def on_plugin(self, data):
        response = self.callback(data)
        computed_signature = hmac.new(self.api_key, msg=response, digestmod=hashlib.sha1).hexdigest()
        return {"response": response, "signature": computed_signature}


def run(plugin, host="https://api.ango.ai"):
    sio = socketio.Client()
    sio.register_namespace(plugin)
    sio.connect(host, namespaces=["/plugin"], wait_timeout=100)
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        logging.getLogger().warning("Plugin Stopped")
