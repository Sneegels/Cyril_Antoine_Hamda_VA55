import time
import _thread
from umqtt.robust import MQTTClient


class MQTTClientThreaded:
    def __init__(
        self,
        client_id,
        broker,
        port=1883,
        user=None,
        password=None,
        loop_delay=1,
    ):
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.user = user
        self.password = password
        self.loop_delay = loop_delay
        self.publish_queue = []
        self.queue_mutex = _thread.allocate_lock()

        self.client = MQTTClient(client_id, broker, port, user, password)

        self._running = False

    class MqttMessage:
        def __init__(self, topic, msg):
            self.topic = topic
            self.msg = msg

    def connect(self):
        """Se connecte au broker et s'abonne si nécessaire."""
        print("Connexion au broker MQTT :", self.broker)
        self.client.connect()
        print("Connecté !")

    def set_callback(self, callback):
        self.client.set_callback(callback)

    def publish(self, topic, msg):
        """Publie un message sur un topic."""
        self.queue_mutex.acquire()
        self.publish_queue.append(self.MqttMessage(topic, msg))
        self.queue_mutex.release()

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print("Abonné au topic :", topic)

    def _loop(self):
        """Boucle interne exécutée dans le thread."""
        while self._running:
            self.client.check_msg()
            self.queue_mutex.acquire()
            while self.publish_queue:
                message = self.publish_queue.pop(0)
                self.client.publish(message.topic, message.msg)
            self.queue_mutex.release()
            time.sleep(self.loop_delay)
        print("Thread MQTT arrêté.")

    def start(self):
        """Démarre le thread."""
        if not self._running:
            self._running = True
            _thread.start_new_thread(self._loop, ())
            print("Thread MQTT démarré.")

    def stop(self):
        """Arrête le thread et déconnecte le client."""
        self._running = False
        # Attendre un petit moment pour que le thread termine
        time.sleep(self.loop_delay + 0.1)
        try:
            self.client.disconnect()
        except:
            pass
        print("Client MQTT déconnecté.")
