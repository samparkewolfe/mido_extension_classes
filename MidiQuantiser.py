import mido-extention-classes.MidiNote as MidiNote
import copy

"""
MidiQuantiser Class

Details:
    Restricts the pitch's of a list of MidiNote objects to a scale.

Usage:
    process (notes, scale, pitch = 16)

        Args:
            notes: a list of MidiNote objects.
            scale: a list of intervals of a scale (see below for examples).
            pitch: the first note of the scale. e.g. 16 is an E.

Examples:
    major =            [2,2,1,2,2,2,1]
    dorian =           [2,1,2,2,2,1,2]
    lydian =           [2,2,2,1,2,2,1]
    mixolydian =       [2,2,1,2,2,1,2]
    aeolian =          [2,1,2,2,1,2,2]
    harmonic_minor =   [2,1,2,2,2,2,1]
"""

class MidiQuantiser:

    def __init__(self):
        print ("Made MidiQuantiser")

    def process (self, notes, scale, pitch = 16):

        newNotes = copy.deepcopy(notes)
        notesOfScale = []
        intervalsIterator = 0
        startingPitch = pitch
        notesOfScale.append(pitch)

        for i in range (128):
            pitch = pitch + scale[intervalsIterator]
            notesOfScale.append(pitch)
            intervalsIterator = intervalsIterator + 1
            intervalsIterator = intervalsIterator % len (scale)

        for note in newNotes:
            if (note.pitch >= startingPitch and note.pitch < 128):
                note.pitch = min(notesOfScale, key=lambda x:abs(x - round(note.pitch)))

        return newNotes
