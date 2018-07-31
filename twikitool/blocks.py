class TagUpgrader(object):
    """docstring for TagUpgrader"""
    
    def __init__(self):
        super(TagUpgrader, self).__init__()

        self.registered_tags = [
            TestTag,
            Comment,
            Ignore,
            Answer,
            PaperQuote,
            BorderDiv,
            Input,
            ]

    def upgrade(self, tag):
        for C in self.registered_tags:
            if C.name == tag.name:
                tag.__class__ = C
                break
        else:
            raise ValueError(
                'Could not process tag {0}; \'{1}\' is not a valid tag'
                .format(tag, tag.name)
                )

class Block(object):
    """docstring for Block"""
    def __init__(self):
        super(Block, self).__init__()

class TextBlock(Block):
    """docstring for TextBlock"""
    def __init__(self, text):
        super(TextBlock, self).__init__()
        self.text = text
        self.is_text = True
        self.is_tag  = False

    def __str__(self):
        if len(self.text) > 30:
            text = self.text[:30] + '...'
        else:
            text = self.text
        return '<TextBlock "{0}">'.format(text)

class BaseTag(Block):
    """docstring for BaseTag"""
    def __init__(self, name='base', opening=True, options=None):
        super(BaseTag, self).__init__()
        self.name = name
        if options is None:
            self.options = {}
        else:
            self.options = options
        self.opening = opening
        self.is_text = False
        self.is_tag  = True

        self.no_closing_tag = False


    def __eq__(self, other):
        return (
            self.name == other.name
            and self.opening == other.opening
            and self.options == other.options
            )

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __str__(self):
        option_str = ' '.join([ '{0}={1}'.format(key, value) for key, value in self.options.iteritems() ])
        if option_str != '':
            option_str = ' ' + option_str
        return '<{0}{1}{2}>'.format(
            '' if self.opening else '/',
            self.name,
            option_str
            )

    def flatten_text(self, text):
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if len(line) > 0: lines.append(line)
        text = '\n'.join(lines)
        return text

#____________________________________________________________________
# The actual commands

class TestTag(BaseTag):
    """docstring for TestTag"""
    name = 'testtag'

    def __init__(self):
        super(TestTag, self).__init__()

    def process(self, text):
        return '[TESTTAG]' + text + '[/TESTTAG]'

class Comment(BaseTag):
    """docstring for Comment"""
    name = 'comment'

    def __init__(self):
        super(Comment, self).__init__()

    def process(self, text):
        text = text.strip()
        color = self.options.get('color', 'blue').upper()
        prefix = '%{0}%\n*<literal>\n'.format(color)
        suffix = '\n</literal>*\n%ENDCOLOR%<br>'
        return prefix + text + suffix

class Answer(BaseTag):
    """docstring for Answer"""
    name = 'answer'

    def __init__(self):
        super(Answer, self).__init__()

    def process(self, text):
        text = text.strip()
        if len(text) == 0: return ''
        text = self.flatten_text(text)

        if 'color' in self.options:
            prefix = '%{0}%\n*'.format(self.options['color'])
            suffix = '*\n%ENDCOLOR%'
        else:
            prefix = '<b>'
            suffix = '</b>\n'
        return prefix + text + suffix

class PaperQuote(BaseTag):
    """docstring for PaperQuote"""
    name = 'paperquote'

    def __init__(self):
        super(PaperQuote, self).__init__()

    def process(self, text):
        text = text.strip()
        prefix = '<br>\n_<literal>'
        suffix = '</literal>_\n<br>'
        return prefix + text + suffix

class Ignore(BaseTag):
    """docstring for Ignore"""
    name = 'ignore'

    def __init__(self):
        super(Ignore, self).__init__()

    def process(self, text):
        return ''

class BorderDiv(BaseTag):
    """docstring for BorderDiv"""
    name = 'borderdiv'

    def __init__(self):
        super(BorderDiv, self).__init__()

    def process(self, text):
        text = text.strip()
        if len(text) == 0: return ''
        text = self.flatten_text(text)

        prefix = '<div style="border:1px solid silver; background-color:#EFEFEF; padding:5px;">'
        suffix = '</div>\n'
        return prefix + text + suffix



class Input(BaseTag):
    """docstring for Input"""
    name = 'input'

    def __init__(self):
        super(Input, self).__init__()
        self.no_closing_tag = True

    def process(self):
        return ''






