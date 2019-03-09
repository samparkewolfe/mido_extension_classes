"""

Put this file in the parent directory of the classes.

run the following command from the terminal:
    python mido-extension-class-test.py

"""

from mido_extension_classes import MidiNote
from mido_extension_classes import MidiNoteWithLength
from mido_extension_classes import MidiLoader
from mido_extension_classes import MidiSaver
from mido_extension_classes import MidiNoteWithLengthBuffer
from mido_extension_classes import MidiConverter

midifile = "mido_extension_classes/mido_extension_classes_test.mid"

midiLoader = MidiLoader()
notes = midiLoader.load(midifile)

midiConverter = MidiConverter()
midiConverter.convert (notes)
midiConverter.convert (notes)

MidiSaver = MidiSaver(notes)
MidiSaver.write('MidiConverted')
