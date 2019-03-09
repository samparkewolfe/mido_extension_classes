"""
Midi Note Class

Details:
    This is the standart MidiNote object.

Variables:
    pitch: Midi Pitch between 0 and 127.
    velocity: Midi Velocity between 0 and 127.
    time: the time in seconds that this midi note comes after the previous note.

"""

class MidiNote(object):
    def __init__(self, pitch, velocity, time):
        self.pitch = pitch
        self.velocity = velocity
        self.time = time

    def __cmp__(self, other):
        return cmp((self.pitch, self.velocity, self.time),
                    (other.pitch, other.velocity, other.time))

    def __str__(self):
        return ('Midi Note: ' +
                'note: ' + str(self.pitch) + ' ' +
                'velocity: ' + str(self.velocity) + ' ' +
                'time: ' + str(self.time))

    def toList(self):
        return [self.pitch, self.velocity, self.time]

    def getTime(self):
        return self.time

    def __add__(self, other):
        return MidiNote(self.pitch + other.pitch,
                        self.velocity + other.velocity,
                        self.time + other.time)

    def __sub__(self, other):
        return MidiNote(self.pitch - other.pitch,
                        self.velocity - other.velocity,
                        self.time - other.time)
