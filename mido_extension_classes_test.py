"""

Put this file in the parent directory of the classes to use.

run the following command from the terminal:
    python mido-extension-class-test.py
   
"""

from mido_extension_classes import MidiNote
from mido_extension_classes import MidiLoader
from mido_extension_classes import MidiNoteSaver
from mido_extension_classes import MidiNoteBuffer

midifile = "mido_extension_classes_test.mid"
midiLoader = MidiLoader()
midiLoader.load(midifile)

midiNoteSaver = MidiNoteSaver(midiLoader.getNotes())

midiNoteSaver.write('MidiConverted')
