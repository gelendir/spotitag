from datetime import datetime


class Ticker:

    def __init__(self):
        self.stamps = []

    def tick(self):
        self.stamps.append(datetime.now())
        if len(self.stamps) > 8:
            self.stamps.pop(0)

    def tapped_bpm(self):
        bpm = 0
        for pos in range(1, len(self.stamps)):
            current = self.stamps[pos]
            previous = self.stamps[pos-1]
            delta = (current - previous).total_seconds()
            bpm += 1 / delta * 60

        return 0 if bpm == 0 else bpm / (len(self.stamps) - 1)
