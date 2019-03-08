import mido_extension_classes.MidiNote as MidiNote

"""
MidiNoteBuffer Class

Details:
    This is a basic vector/list type object which should hold a collection of the custom MidiNote objectself.
    What's special about this object is it's interface with MidiNotes represented as lists or as MidiNote objects.

Usage:
    pushBackInfo(midiInfo)
        Appends a MidiNote object to an internal list of MidiNote objects, converting a raw list of values representing a midi note.
        Args:
            midiInfo: a 4 dimentional list representing a notes pitch, velocity, time and length

    pushBackNote(self, note)
        Appends a MidiNote object to the internal list of MidiNote objects.
        Args:
            note: a MidiNote object.

    getNotesAsList()
        returns all the notes in the interal list of MidiNote objects as a lists.
"""

class MidiNoteBuffer:
    def __init__(self):
        self.notes = []
        print("New Midi Buffer Made")

    def setNotes(self, notes):
        self.notes = notes
        print ("Set Notes")

    def getNotes(self):
        return self.notes

    def pushBackInfo(self, midiInfo):
        self.notes.append(self.convertMidiInfoToMidiNote(midiInfo))

    def pushBackNote(self, note):
        self.notes.append(note)

    def convertMidiInfoToMidiNote(self, midiInfo):
        note = MidiNote(pitch       = midiInfo[0],
                        velocity    = midiInfo[1],
                        time        = midiInfo[2],
                        length      = midiInfo[3])

        return note

    def getNotesAsList(self):
        list = []
        for note in self.notes:
            list.append(note.toList())

        return list
