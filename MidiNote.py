"""
Midi Note Class

Details:
    This is the custom MidiNote object this library uses.
    This class is different than a standard midi note because it does not use the "note on -> note off" method.
    Instead this object has a "length" variable which represents how long the note should last.

Variables:
    pitch: Midi Pitch between 0 and 127.
    velocity: Midi Velocity between 0 and 127.
    time: the time in seconds that this midi note comes after the previous note.
    length: the amount of time this note lasts for in seconds.
"""

class MidiNote(object):
    def __init__(self, pitch, velocity, time, length):
        self.pitch = pitch
        self.velocity = velocity
        self.time = time
        self.length = length

    def __cmp__(self, other):
        return cmp((self.pitch, self.velocity, self.time, self.length),
                    (other.pitch, other.velocity, other.time, other.length))

    def __str__(self):
        return ('Midi Note: ' +
                'note: ' + str(self.pitch) + ' ' +
                'velocity: ' + str(self.velocity) + ' ' +
                'time: ' + str(self.time) + ' ' +
                'length: ' + str(self.length))

    def toList(self):
        return [self.pitch, self.velocity, self.time, self.length]

    def getTime(self):
        return self.time

    def __add__(self, other):
        return MidiNote(self.pitch + other.pitch,
                        self.velocity + other.velocity,
                        self.time + other.time,
                        self.length + other.length)

    def __sub__(self, other):
        return MidiNote(self.pitch - other.pitch,
                        self.velocity - other.velocity,
                        self.time - other.time,
                        self.length - other.length)
