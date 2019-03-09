
import mido_extension_classes.MidiNote as MidiNote
from mido import Message, MidiFile, MidiTrack, MetaMessage, second2tick
import copy

"""
MidiSaver Class

Details:
    This object converts a list of custom MidiNote objects back to the mido midi message format and writes it to file.

Usage:
    MidiSaver(notesToWrite, ticks_per_beat = 480)
        Constructor copys a list of MidiNote objects to write and sets the ticks_per_beat the user wants to write the midi file to.

        Args:
            notesToWrite: a list of MidiNote objects to write to file.
            ticks_per_beat: (see https://mido.readthedocs.io/en/latest/midi_files.html)

    write(fileName):
        Writes a list of MidiNote objects to file.
        Args:
            fileName: the absolute path to write the midi file to (not including the .mid extension)
"""

class MidiSaver:

    def __init__(self, notesToWrite, ticks_per_beat = 480):
        self.notesToWrite = []
        self.notesToWrite = copy.deepcopy(notesToWrite)
        self.ticks_per_beat = ticks_per_beat
        print("New Midi Saver Made")

    def write(self, fileName):
        self.restrictNoteRanges(self.notesToWrite)

        self.convertTimesFromSecondsToTicks(self.notesToWrite)

        self.writeMidiFile(self.notesToWrite, fileName)
        print("MidiNotes have been written to file")

    def restrictNoteRanges(self, notes):
        for note in notes:
            note.pitch = int(round(note.pitch))
            note.velocity = int(round(note.velocity))

            if(note.pitch < 0):
                note.pitch = 0
            if(note.velocity < 0):
                note.velocity = 0
            if(note.time < 0):
                note.time = 0

            if(note.pitch > 127):
                note.pitch = 127
            if(note.velocity > 127):
                note.velocity = 127

    def convertTimesFromSecondsToTicks(self, notes):
        for note in notes:
            note.time = int(second2tick(note.time, self.ticks_per_beat, 500000))

    def writeMidiFile(self, notes, fileName):
        midiOut = MidiFile(type=1, ticks_per_beat = self.ticks_per_beat)

        track = MidiTrack()

        for note in notes:
            # print(note)
            track.append (Message ('note_on',
                                   note = note.pitch,
                                   velocity = note.velocity,
                                   time = note.time))

        track.append (MetaMessage ('end_of_track', time=0))

        midiOut.tracks.append(track)

        midiOut.save(fileName + '.mid')
