import mido_extension_classes.MidiNote as MidiNote

"""
MidiNoteWithLengthBuffer Class

Details:
    This is a basic vector/list type object which should hold a collection of the custom MidiNoteWithLength objects.
    What's special about this object is it's interface with MidiNotes represented as lists or as MidiNote objects.
    This makes processing you list of midinotes with the rest of python a little bit easier, rather than having to convert them to lists all the time.

Usage:
    pushBackInfo(midiInfo)
        Appends a MidiNoteWithLength object to an internal list of MidiNoteWithLength objects, converting a raw list of values representing a midi note.
        Args:
            midiInfo: a 4 dimentional list representing a notes pitch, velocity, time and length

    pushBackNote(self, note)
        Appends a MidiNoteWithLength object to the internal list of MidiNoteWithLength objects.
        Args:
            note: a MidiNoteWithLength object.

    getNotesAsList()
        returns all the notes in the interal list of MidiNote objects as a lists.
"""

class MidiNoteWithLengthBuffer:
    def __init__(self):
        self.notes = []
        print("New Midi Buffer Made")

    def setNotes(self, notes):
        self.notes = notes
        print ("Set Notes")

    def getNotes(self):
        return self.notes

    def pushBackInfo(self, midiInfo):
        self.notes.append(self.convertMidiInfoToMidiNoteWithLength(midiInfo))

    def pushBackNote(self, note):
        self.notes.append(note)

    def convertMidiInfoToMidiNoteWithLength(self, midiInfo):
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
