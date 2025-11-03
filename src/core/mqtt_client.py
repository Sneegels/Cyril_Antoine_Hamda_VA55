import time
import _thread
from umqtt.simple import MQTTClient
import network


class MQTTClientThreaded:
    def __init__(
        self,
        client_id,
        broker,
        port=1883,
        user=None,
        password=None,
        topic_sub=None,
        loop_delay=1,
    ):
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.user = user
        self.password = password
        self.topic_sub = topic_sub
        self.loop_delay = loop_delay

        self.client = MQTTClient(client_id, broker, port, user, password)
        self.client.set_callback(self.on_message)

        self._running = False

    def connect(self):
        """Se connecte au broker et s'abonne si nécessaire."""
        print("Connexion au broker MQTT :", self.broker)
        self.client.connect()
        print("Connecté !")
        if self.topic_sub:
            self.client.subscribe(self.topic_sub)
            print("Abonné au topic :", self.topic_sub)

    def on_message(self, topic, msg):
        """Callback appelé quand un message est reçu."""
        print("Message reçu sur", topic.decode(), ":", msg.decode())

    def publish(self, topic, msg):
        """Publie un message sur un topic."""
        self.client.publish(topic, msg)

    def _loop(self):
        """Boucle interne exécutée dans le thread."""
        while self._running:
            self.client.check_msg()
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
