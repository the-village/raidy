import json


class VkKeyboardColors:
    PRIMARY = "primary" # blue
    SECONDARY = "secondary" # white
    NEGATIVE = "negative" # red
    POSITIVE = "positive" # green


class VkKeyboard:
    def __init__(self, one_time):
        self.one_time = one_time
        self.lines = [[]]
        self.keyboard = {
               "one_time":self.one_time,
               "buttons": self.lines
            }

    def new_button(self, label, color, payload=None):
        now_line = self.lines[-1]
        payload = payload if payload != None else json.dumps({"command": label})
        button = {"action": {"type": "text", "payload": payload, "label": label}, "color": color}
        now_line.append(button)

    def new_line(self):
        self.lines.append([])

    def get_keyboard(self):
        return json.dumps(self.keyboard)
