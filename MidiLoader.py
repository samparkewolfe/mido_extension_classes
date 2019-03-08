from mido import MidiFile
from mido import tick2second
import mido-extention-classes.MidiNote as MidiNote

"""
Midi Loader Class

Details:
    This object loads a midi file using mido.
    Extracts the midi notes leaving behind all other midi event types (e.g. tempo_change, expression)
    Converts all midi notes into the custom MidiNote class.
        This involes removing all the note off messages and creating a new note type with a "note length variable" instead (see MidiNote.py)

Usage:
load (locationOfMidiFile)
    Loads a midi file using mido's "MidiFile" class.
    Fills interal list "notes" with MidiNote objects extracted from file.
        Args:
            locationOfMidiFile: absolute location to a .mid file.
        Return:
            Nothing


getNotes()
    returns the list of MidiNote objects held interally in this object.
        Args:
            None
        Return:
            list of MidiNote objects held interally in this object.

All other functions are not intended for users use.

Warning: If the midi file is multi-track, the note information of all tracks will be concatinated after one and other.
"""

class MidiLoader:
    def __init__(self):
        self.notes = []
        self.ticks_per_beat = -1

    def load(self, locationOfMidiFile):
        try:
            midiFile = MidiFile(locationOfMidiFile)
        except IOError:
            print("Bad Midi File")
            return

        self.ticks_per_beat = midiFile.ticks_per_beat

        self.extractMidiNotesFromMidoFile(self.notes, midiFile)

        if(self.calculateNoteLengths(self.notes) == "broken"):
            self.notes = []
            return

        # take away note offs and recalculate times relative to previouse notes.
        self.filterNoteOffs(self.notes)

        self.convertNoteTimesFromTicksToSeconds(self.notes, midiFile)

        print("Loaded Midi File:", locationOfMidiFile)


    def getNotes(self):
        return self.notes

    def convertNoteTimesFromTicksToSeconds(self, notes, midiFile):
        for note in notes:
            note.time = tick2second(note.time, midiFile.ticks_per_beat, 500000)
            note.length = tick2second(note.length, midiFile.ticks_per_beat, 500000)

    # Strips away all non noteOn notes from file
    # Recalculates new note times with the other notes taken away
    def extractMidiNotesFromMidoFile (self, notes, midiFile):
        # Recalculate times for just note information
        for trackIter, track in enumerate(midiFile.tracks):
            # print('Track {}: {}'.format(trackIter, track.name))

            for rawMidiMessageIter, rawMidiMessage in enumerate(track):

                # if message is a note
                if (rawMidiMessage.type == 'note_on'):
                    # print("Note Message:", rawMidiMessage)

                    # Skip the first note
                    if(len(notes) == 0):
                        notes.append (MidiNote (pitch = rawMidiMessage.note,
                                                    velocity = rawMidiMessage.velocity,
                                                    time = 0,
                                                    length = -1))
                        continue

                    previousRawMidiMessageIter = -1
                    timeBeforeMessage = rawMidiMessage.time

                    while (True):

                        previousMessage = track[rawMidiMessageIter + previousRawMidiMessageIter]
                        # print("    ", "Previous Midi Message:", previousMessage)

                        # Is the next midi message a note message?
                        if (previousMessage.type == 'note_on'):
                                # print("    ", "Previous Midi Message Is a Note:", previousMessage)
                                break

                        timeBeforeMessage = timeBeforeMessage + previousMessage.time


                        # print("    ", "Time Before Message:", timeBeforeMessage)
                        previousRawMidiMessageIter = previousRawMidiMessageIter - 1

                    # print("Total Time:", timeBeforeMessage)
                    notes.append (MidiNote (pitch = rawMidiMessage.note,
                                            velocity = rawMidiMessage.velocity,
                                            time = timeBeforeMessage,
                                            length = -1))


    def calculateNoteLengths(self, notes):

        for noteIter, note in enumerate(notes):

            if (note.velocity > 0):
                # print("Note On Message:", note)

                pitch = note.pitch
                nextMidiNoteIter = 1

                timeAfterNoteOn = 0

                while (True):
                    if (noteIter + nextMidiNoteIter >= len(notes)):
                        return "Broken"

                    nextNote = notes[noteIter + nextMidiNoteIter]

                    # print ("    ", "Next Midi Note:", nextNote)
                    timeAfterNoteOn = timeAfterNoteOn + nextNote.time

                    # Is the next note the the noteOff?
                    if ((nextNote.pitch == pitch) and (nextNote.velocity == 0)):
                        # print("    ", "Next Midi Note Is Note Off:", nextNote)
                        break

                    # print("    ", "Time Since Note On:", timeAfterNoteOn)
                    nextMidiNoteIter = nextMidiNoteIter + 1

                note.length = timeAfterNoteOn


    # Time is recalculated after removing each note off.
    def filterNoteOffs (self, notes):

        justNoteOns = []

        for noteIter, note in enumerate (notes):

            if (note.velocity > 0):

                # print("Note Message:", note)

                # Skip the first note
                if(len(justNoteOns) == 0):
                    justNoteOns.append(note)
                    continue

                previousNoteIter = -1
                timeBeforeCurrentNote = note.time

                while (True):

                    previousNote = notes[noteIter + previousNoteIter]
                    # print("    ", "Previous Note:", previousNote)

                    # Is the previouse note a noteOn?
                    if (previousNote.velocity > 0):
                            # print("    ", "Previous note is a noteOn:", previousNote)
                            break

                    timeBeforeCurrentNote = timeBeforeCurrentNote + previousNote.time


                    # print("    ", "Time Before Current Note:", timeBeforeCurrentNote)
                    previousNoteIter = previousNoteIter - 1

                # print("Total Time:", timeBeforeCurrentNote)
                note.time = timeBeforeCurrentNote
                justNoteOns.append(note)

        self.notes = justNoteOns
