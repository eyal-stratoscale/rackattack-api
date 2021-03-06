import threading
import logging
import time

HEARTBEAT_OK = "OK"


class HeartBeat(threading.Thread):
    def __init__(self, client):
        self._client = client
        self._ids = []
        threading.Thread.__init__(self)
        self.daemon = True
        threading.Thread.start(self)

    def register(self, id):
        assert id not in self._ids
        self._ids.append(id)

    def unregister(self, id):
        assert id in self._ids
        self._ids.remove(id)

    def run(self):
        try:
            while True:
                time.sleep(5)
                if len(self._ids) == 0:
                    continue
                response = self._client.call('heartbeat', ids=self._ids)
                if response != HEARTBEAT_OK:
                    logging.error("Rackattack heartbeat failed: '%(message)s'", dict(message=response))
                    raise Exception("Rackattack heartbeat failed: '%s'" % response)
        except:
            logging.exception("Rackattack heartbeat thread dies")
            raise
        finally:
            logging.error("heartbeat thread notifies client about failure")
            self._client.heartbeatFailed()
