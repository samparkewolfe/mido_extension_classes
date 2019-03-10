# Mido Extension Classes

These classes extend the [Mido](https://github.com/mido/mido) python library for midi.

These classes were originally made for doing machine learning on single track midi files.

The main purpose of these classes is to convert midi notes from the standard encoding of "note on" and "note off" messages into one midi note with a "length" attribute (and back).

The workflow handles two different midi note objects
* MidiNote: The standard encoding of "note on" and "note off"
* MidiNoteWithLength: Removing all the "note off" midi notes in a sequence and giving each "note on" a length attribute.

The loader class also extracts only midi note data, cleaning messy midi files.

#### Requirements
* mido (pip install mido)
* copy (pip install copy)
