# -*- encoding: utf-8 -*-
#
# Create a keyboard based on letter frequencies
# Copyright (C) 2015  Tryggvi Björgvinsson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from bs4 import BeautifulSoup
from collections import Counter
from string import lowercase
import re
import json
import argparse

class KeyboardCreator(object):
    """
    Class to create a keyboard based on letter frequencies.
    """

    def __init__(self, keyboard=None, alternatives=None, *args, **kwargs):
        """
        Initialize keyboard creator with keyboard and alternatives maps
        (optional)
        """

        self.keyboard = keyboard

        self.alternatives = alternatives
        self.inversed_alternatives = None

        if self.alternatives:
            self.inversed_alternatives = {
                character:k for (k,v) in self.alternatives.iteritems()
                            for character in v}

        # We want at least the ascii characters to be covered so we add them
        # and subtract them so we won't affect the count
        main_characters = map(self.get_main_character, lowercase)
        self.characters = Counter(main_characters)
        self.characters.subtract(main_characters)

    def get_main_character(self, character):
        """
        Get the main keyboard character. This is mostly for mobile keyboards
        where each key might have more than one character associated with it
        e.g. á might be an alternative key for a, but a would be the main
        character
        """
        # We can only do this if inversed_alternatives is not None, i.e. if
        # alternatives have been provided and if so we just get and default
        # to the provided character
        if self.inversed_alternatives:
            return self.inversed_alternatives.get(character, character)
        else:
            return character

    def get_all_values(self, character, delimiter=u'/'):
        """
        Get all values for a given character. This is mostly for mobile
        keyboards where each key might have more than one character
        associated with it, so we want to return all of them joined by
        a delimiter
        """
        if self.alternatives:
            alternatives = self.alternatives.get(character, [])
        else:
            alternatives = []
        return delimiter.join([character] + alternatives)

    def load_from_text(self, text):
        """
        Add characters in provided text to the count. We only add the main
        characters to the count (so alternative characters are added to the
        main character count).
        """
        text_chars = map(self.get_main_character,
                         re.findall(r'[^\W\d_]', text, flags=re.UNICODE))

        self.characters.update(text_chars)

    def load_from_file(self, filehandler):
        """
        Load and add count for all characters in an xml file. The xml file
        should be provided as a file handler. This will read in the xml file
        and grab all text in it and append that to the count.
        """
        data = filehandler.read()

        # Text might be in xml or html or something, not just plain text
        # so we pass it through beautiful soup to grab all the text
        soup = BeautifulSoup(data)
        text = soup.get_text().lower()

        self.load_from_text(text)

    @property
    def most_used_keys(self):
        """
        Return the most common keys based on loaded text
        """
        return [k for (k,v) in self.characters.most_common()]

    def print_keyboard(self):
        """
        Print a representation of the keyboard, based on a layout provided
        """

        if not self.keyboard:
            print "No keyboard layout provided"
            return

        positions = {}
        max_key_length = 0
        for (position, key) in enumerate(self.most_used_keys):
            all_values = self.get_all_values(key)
            positions[position] = all_values
            max_key_length = max(len(all_values), max_key_length)

        keyboard_layout = u''
        for keyboard_row in self.keyboard:
            for keyboard_position in keyboard_row:
                if keyboard_position in positions:
                    keys = positions.pop(keyboard_position)
                else:
                    keys = u'⌨'
                padding = (max_key_length - len(keys))/2
                keyboard_layout += u'[ {pad}{key}{pad} ]'.format(
                    pad=u' '*padding, key=keys)

            keyboard_layout += u'\n'

        if positions:
            print positions
            print "Keys not mapped:", u' - '.join(positions.values())
            
        print keyboard_layout[:-1]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--alternatives', nargs=1)
    parser.add_argument('-k', '--keyboard', nargs=1)
    parser.add_argument('files', help="Text file for character counting",
                        nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if args.keyboard:
        with open(args.keyboard[0]) as keyboard_layout:
            keyboard = [[int(pos) for pos in line.split()]
                        for line in keyboard_layout if line.strip() != '']
    else:
        keyboard = None

    if args.alternatives:
        with open(args.alternatives[0]) as alternatives:
            alternatives = json.loads(alternatives.read())

    else:
        alternatives=None

    keyboard = KeyboardCreator(keyboard=keyboard, alternatives=alternatives)

    for filename in args.files:
        with open(filename) as textfile:
            keyboard.load_from_file(textfile)

    keyboard.print_keyboard()
