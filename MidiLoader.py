from mido import MidiFile
from mido import tick2second
import mido_extension_classes.MidiNote as MidiNote

"""
Midi Loader Class

Details:
    This object loads a midi file using mido.
    Extracts the midi notes leaving behind all other midi event types (e.g. tempo_change, expression)
    Converts all the midi midi information into this libraries custom MidiNote class.

Usage:
load (locationOfMidiFile)
    Loads a midi file using mido's "MidiFile" class.
    returns a list filled with MidiNote objects extracted from file.
        Args:
            locationOfMidiFile: absolute location to a .mid file.
        Return:
            list of MidiNote objects held interally in this object.


All other functions are not intended for users use.

Warning: If the midi file is multi-track, the note information of all tracks will be concatinated after one and other.
"""

class MidiLoader:
    def __init__ (self):
        self.ticks_per_beat = -1

    def load (self, locationOfMidiFile):
        try:
            midiFile = MidiFile(locationOfMidiFile)
        except IOError:
            print("Bad Midi File")
            return

        self.ticks_per_beat = midiFile.ticks_per_beat

        notes = []

        self.extractMidiNotesFromMidoFile(notes, midiFile)

        self.convertNoteTimesFromTicksToSeconds(notes, midiFile)

        print("Loaded Midi File:", locationOfMidiFile)

        return notes

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
                                                time = 0))
                        continue

                    previousRawMidiMessageIter = -1
                    timeBeforeMessage = rawMidiMessage.time

                    while (True):

                        previousMessage = track[rawMidiMessageIter + previousRawMidiMessageIter]

                        # Is the next midi message a note message?
                        if (previousMessage.type == 'note_on'):
                                break

                        timeBeforeMessage = timeBeforeMessage + previousMessage.time

                        previousRawMidiMessageIter = previousRawMidiMessageIter - 1

                    notes.append (MidiNote (pitch = rawMidiMessage.note,
                                            velocity = rawMidiMessage.velocity,
                                            time = timeBeforeMessage))


    def convertNoteTimesFromTicksToSeconds(self, notes, midiFile):
        for note in notes:
            note.time = tick2second(note.time, midiFile.ticks_per_beat, 500000)
