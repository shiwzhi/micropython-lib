import json

class HADevice:
    def __init__(self, deviceName) -> None:
        self.deviceName = deviceName
        self.sensor_list = []

    def get_sensor(self, name, device_class="", unit="", icon=""):
        s = HAsensor(name=name, deviceName=self.deviceName,
                     device_class=device_class, unit=unit, icon=icon)
        self.sensor_list.append(s)
        return s

    def get_state_topic(self):
        return f"homeassistant/sensor/{self.deviceName}/state"

    def get_state_payload(self):
        payload = {}
        for i in self.sensor_list:
            payload[i.name] = i.value
        return json.dumps(payload)

    def get_list_of_topic_and_payload(self):
        list_of_topic_payload = []
        for s in self.sensor_list:
            config_topic = s.get_config_topic()
            config_payload = s.get_config_payload()
            list_of_topic_payload.append((config_topic, config_payload))
        state_topic = self.get_state_topic()
        state_payload = self.get_state_payload()
        list_of_topic_payload.append((state_topic, state_payload))
        return list_of_topic_payload


class HAsensor:
    def __init__(self, name, deviceName, device_class, unit, icon) -> None:
        self.name = name
        self.device_class = device_class
        self.unit = unit
        self.icon = icon
        self.deviceName = deviceName
        self.value = 0

    def update_value(self, value):
        self.value = value

    def get_config_topic(self):
        topic = f"homeassistant/sensor/{self.deviceName}{self.name}/config"
        return topic

    def get_config_payload(self):
        payload = {
            "name": self.name,
            "state_topic": f"homeassistant/sensor/{self.deviceName}/state",
            "value_template": f"{{{{value_json.{self.name}}}}}"}

        if self.device_class != "":
            payload['device_class'] = self.device_class
        if self.unit != "":
            payload['unit_of_measurement'] = self.unit
        if self.icon != "":
            payload['icon'] = self.icon

        return json.dumps(payload)