status = ['Not started', 'Starting', 'Running', 'Stopping']


class Resender:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.status = status[0]

    def start(self):
        self.status = status[2]
        return f'Start {self.name}'

    def stop(self):
        self.status = status[0]
        return f'Stop {self.name}'

    def restart(self):
        self.status = status[2]
        return f'Restart {self.name}'

    def status(self):
        return f'Status {self.name}: {self.status}'
