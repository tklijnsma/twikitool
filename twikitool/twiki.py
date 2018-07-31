
from blocks import *

from collections import deque
import re


class Twiki(object):
    """docstring for Twiki"""
    def __init__(self):
        super(Twiki, self).__init__()
        self.is_processed = False
        self.tagupgrader = TagUpgrader()
        
    def from_twiki_file(self, twiki_file):
        with open(twiki_file, 'r') as twiki_fp:
            self.twiki_text_raw = twiki_fp.read()

    def from_text_string(self, text):
        self.twiki_text_raw = text

    def interpret(self):
        processor = TagProcessor(self.twiki_text_raw)

        text_stack = [ '' ]
        tag_stack = []

        block = processor.next()
        while not(block is False):

            if block.is_text:
                text_stack[-1] += block.text

            elif block.is_tag:
                if block.no_closing_tag:
                    # Some blocks have no closing tag, and are fully specified
                    # by whatever options are supplied
                    text_stack[-1] += block.process()

                else:
                    # Get the appropriate subclass of the tag
                    self.tagupgrader.upgrade(block)

                    if block.opening:
                        # Start new element of the text stack
                        text_stack.append('')
                        # Add the opening block to the queue
                        tag_stack.append(block)
                    else:
                        # Check if last open tag matches this closing tag
                        open_tag = tag_stack.pop()
                        if not block.name == open_tag.name:
                            raise ValueError(
                                'Found closing tag {0}, which does not match the last opening tag {1}'
                                .format(block, open_tag)
                                )

                        # Pop the last element of the text stack, process it, and add back to
                        # last element of the stack
                        active_text_block = text_stack.pop()
                        processed_text_block = open_tag.process(active_text_block)
                        text_stack[-1] += processed_text_block

            block = processor.next()

        if not len(tag_stack) == 0:
            raise ValueError(
                'Some tags were not closed; Remaining open tags:\n{0}'
                .format(tag_stack)
                )

        if not len(text_stack) == 1:
            raise ValueError(
                'Length of text stack is {0}, not 1; This can\'t be right. Full text stack:\n{1}'
                .format(len(text_stack), text_stack)
                )

        self.processed_text = text_stack[0]
        self.is_processed = True


class TagProcessor(object):
    """docstring for TagProcessor"""
    def __init__(self, text):
        super(TagProcessor, self).__init__()
        self.text = text
        self.n = len(text)
        self.i = 0
        self.segment_length = 200
        
    def next(self):
        if self.i == self.n-1: # EOF
            return False
        elif self.text[self.i:self.i+2] == '<@':
            return self.next_tag()
        else:
            return self.next_textblock()

    def next_textblock(self):
        # This block will be pure text
        literal_mode = False
        for i in xrange(self.i, self.n):
            if self.text[i:i+9] == '<literal>':
                literal_mode = True
            if self.text[i:i+10] == '</literal>':
                literal_mode = False
            if not(literal_mode) and self.text[i:i+2] == '<@':
                text_block = self.text[self.i:i]
                self.i = i
                break
        else:
            text_block = self.text[self.i:]
            self.i = self.n-1
        return TextBlock(text_block)

    def next_tag(self):
        # This block is a tag
        segment = self.text[self.i:min(self.i+self.segment_length, self.n)]
        match = re.match(
            r'\<\@/*(.*?)>',
            segment
            )
        if not match:
            raise ValueError('Could not determine tag; raw text:\n{0}'.format(segment))

        opening = False if self.text[self.i+2] == '/' else True

        components = match.group(1).split()

        tag_name = components[0]

        options = {}
        for option_str in components[1:]:
            if not '=' in option_str:
                raise ValueError(
                    'Error parsing option \'{0}\'; format is option_name=option_value'
                    )
            key, value = option_str.split('=', 1)
            options[key] = value

        self.i += len(match.group())

        tag = BaseTag(
            name = tag_name,
            opening = opening,
            options = options,
            )
        tag.text = match.group()

        if tag.name == 'input':
            # Special case; expand inputs now in order to process correctly
            self.expand_input(tag)
            return TextBlock('')

        return tag


    def preview_segment(self, n=7):
        segment = self.text[self.i:min(self.i+n, self.n)]
        segment = segment.replace('\n', '\\n')
        return segment

    def expand_input(self, tag):
        input_file = tag.options['file']
        with open(input_file, 'r') as input_fp:
            input_raw_text = input_fp.read()
        self.text = self.text[:self.i] + input_raw_text + self.text[self.i:]
        self.n = len(self.text)


