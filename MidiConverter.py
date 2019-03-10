import mido_extension_classes.MidiNote as MidiNote
import mido_extension_classes.MidiNoteWithLength as MidiNoteWithLength
import copy

"""
MidiConverter Class
Details:
    Converts a list of either MidiNote or MidiNoteWithLength objects into the oposite type.
    
Usage:
convert (notesToConvert)
    Takes in a list of MidiNote or MidiNoteWithLength objects and returns a list of midi notes of the opposite type.
    e.g. If given a list of MidiNote objects, the function will return a list of MidiNoteWithLength objects.
    This process would involve calculating the length of each note in the list and then removing all the note off messages.
    If given a list of MidiNoteWithLength objects, the function will create an "off" MidiNote object for each midi note at the correct time.
    Then replace each MidiNoteWithLength with a MidiNote object with the same pitch, velocity and time but without the length attribute.

        Args:
            notesToConvert: a list of MidiNote or MidiNoteWithLength objects.
        Return:
            New list of MidiNote or MidiNoteWithLength objects.
            
All other functions are not intended for users use.

Warning: The type of midi note in the list has to be the same for all midi notes in the list.
"""

class MidiConverter:
    def __init__(self):
        print ("Created MidiConverter Class")

    def convert (self, notesToConvert):

        notes = copy.deepcopy (notesToConvert)

        if (type (notes [0]) == MidiNote):
            self.convertMidiNotesToMidiNotesWithLengths (notes)

        elif (type (notes [0]) == MidiNoteWithLength):
            self.convertMidiNotesWithLengthsToMidiNotes (notes)

        return notes

    def convertMidiNotesToMidiNotesWithLengths (self, notes):
        print ("Converting Midi Notes To Midi Notes With Lengths")

        notesWithLengths = []

        for note in notes:

            notesWithLengths.append (MidiNoteWithLength (note.pitch,
                                                         note.velocity,
                                                         note.time,
                                                         -1))

        if(self.calculateNoteLengths(notesWithLengths) == "broken"):
            Print ("Could not convert file, Midi File is messed up.")
            return

        self.filterNoteOffs (notesWithLengths)

        return notesWithLengths


    def calculateNoteLengths(self, notes):

        for noteIter, note in enumerate(notes):

            if (note.velocity > 0):

                pitch = note.pitch
                nextMidiNoteIter = 1

                timeAfterNoteOn = 0

                while (True):
                    if (noteIter + nextMidiNoteIter >= len(notes)):
                        return "Broken"

                    nextNote = notes[noteIter + nextMidiNoteIter]

                    timeAfterNoteOn = timeAfterNoteOn + nextNote.time

                    # Is the next note the the noteOff?
                    if ((nextNote.pitch == pitch) and (nextNote.velocity == 0)):
                        break

                    nextMidiNoteIter = nextMidiNoteIter + 1

                note.length = timeAfterNoteOn


    # Time is recalculated after removing each note off.
    def filterNoteOffs (self, notes):

        justNoteOns = []

        for noteIter, note in enumerate (notes):

            if (note.velocity > 0):

                # Skip the first note
                if(len(justNoteOns) == 0):
                    justNoteOns.append(note)
                    continue

                previousNoteIter = -1
                timeBeforeCurrentNote = note.time

                while (True):

                    previousNote = notes[noteIter + previousNoteIter]

                    # Is the previouse note a noteOn?
                    if (previousNote.velocity > 0):
                            break

                    timeBeforeCurrentNote = timeBeforeCurrentNote + previousNote.time


                    previousNoteIter = previousNoteIter - 1

                note.time = timeBeforeCurrentNote
                justNoteOns.append(note)

        return justNoteOns


    def convertMidiNotesWithLengthsToMidiNotes (self, notesWithLengths):
        print ("Converting Midi Notes With Lengths To Midi Notes")

        self.makeTimesRelativeToFirstNote (notesWithLengths)

        self.generateNoteOffs (notesWithLengths)

        self.notesToWrite.sort(key = MidiNoteWithLength.getTime)

        self.makeTimesRelativeToPreviousNote(notesWithLengths)

        notes = []

        for note in notesWithLengths:

            notes.append (MidiNote (note.pitch,
                                    note.velocity,
                                    note.time))

        return notes

    def makeTimesRelativeToFirstNote(self, notes):
        sumOfAllTimes = 0

        for note in notes:
            sumOfAllTimes = sumOfAllTimes + note.time
            note.time = sumOfAllTimes

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
