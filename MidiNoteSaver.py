
import mido_extension_classes.MidiNote as MidiNote
from mido import Message, MidiFile, MidiTrack, MetaMessage, second2tick
import copy

"""
MidiSaver Class

Details:
    This object converts a list of custom MidiNote objects back to the mido midi message format and writes it to file.
    See the MidiNoteLoader for details of the custom MidiNote object format.

Usage:
    MidiSaver(notesToWrite, ticks_per_beat = 480)
        Constructor copys a list of MidiNote objects to write and sets the ticks_per_beat the user wants to write the midi file to.

        Args:
            notesToWrite: a list of MidiNote objects to write to file.
            ticks_per_beat: (see https://mido.readthedocs.io/en/latest/midi_files.html)

    write(fileName):
        Converts all the MidiNoteObjects back to their original format of "note on -> note off" and writes them to file.
        Args:
            fileName: the absolute path to write the midi file to (not including the .mid extension)
"""

class MidiNoteSaver:

    def __init__(self, notesToWrite, ticks_per_beat = 480):
        self.notesToWrite = []
        self.notesToWrite = copy.deepcopy(notesToWrite)
        self.ticks_per_beat = ticks_per_beat
        print ("ticks_per_beat", self.ticks_per_beat)
        print("New Midi Saver Made")

    def write(self, fileName):

        print (self.notesToWrite[0], len(self.notesToWrite))

        self.restrictNoteRanges(self.notesToWrite)

        self.convertTimesFromSecondsToTicks(self.notesToWrite)

        self.makeTimesRelativeToFirstNote(self.notesToWrite)

        self.generateNoteOffs(self.notesToWrite)

        self.notesToWrite.sort(key = MidiNote.getTime)

        self.makeTimesRelativeToPreviousNote(self.notesToWrite)

        self.writeMidiFile(self.notesToWrite, fileName)
        print("MidiNotes have been written to file")

    def convertTimesFromSecondsToTicks(self, notes):
        for note in notes:
            note.time = int(second2tick(note.time, self.ticks_per_beat, 500000))
            note.length = int(second2tick(note.length, self.ticks_per_beat, 500000))
        print ("converted times")

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
            if(note.length < 0):
                note.length = 0

            if(note.pitch > 127):
                note.pitch = 127
            if(note.velocity > 127):
                note.velocity = 127

    def makeTimesRelativeToFirstNote(self, notes):

        notesWithNewTimes = []
        sumOfAllTimes = 0

        for note in notes:
            sumOfAllTimes = sumOfAllTimes + note.time

            noteWithNewTime = MidiNote (pitch = note.pitch,
                                        velocity = note.velocity,
                                        time = sumOfAllTimes,
                                        length = note.length)
            notesWithNewTimes.append(noteWithNewTime)

        self.notesToWrite = notesWithNewTimes

    def generateNoteOffs(self, notes):

        noteOffs = []

        for note in notes:
            noteOff = MidiNote (pitch = note.pitch,
                                velocity = 0,
                                time = note.time + note.length,
                                length = -1)
            noteOffs.append(noteOff)

        notes.extend(noteOffs)


    def makeTimesRelativeToPreviousNote(self, notes):
        reverseIter = len(notes) - 1

        # Convert relative noteOn/Off times to times after the previous message
        for note in reversed(notes):

            if(reverseIter > 0):
                newTime = note.time - notes[reverseIter - 1].time
                note.time = newTime

            reverseIter = reverseIter - 1


    def writeMidiFile(self, notes, fileName):
        midiOut = MidiFile(type=1, ticks_per_beat = self.ticks_per_beat)

        track2 = MidiTrack()

        for note in notes:
            # print(note)
            track2.append(Message('note_on',
                                    note = note.pitch,
                                    velocity = note.velocity,
                                    time = note.time))
        track2.append(MetaMessage('end_of_track', time=0))

        midiOut.tracks.append(track2)

        midiOut.save(fileName + '.mid')
