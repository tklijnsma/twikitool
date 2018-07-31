from unittest import TestCase

import twikitool


class TestProcessor(TestCase):

    def test_basic_tag_finding(self):
        """Tests a sequence of block finding with text and options """

        text = """<@question>T1<@/question>T2<@answer color=red>T3<@/answer>"""
        processor = twikitool.TagProcessor(text)

        print 'Test 1'
        print 'Starting from position {0}; \"{1}...\"'.format(processor.i, processor.preview_segment())
        tag = processor.next()
        expected = twikitool.BaseTag(
            name = 'question',
            opening = True,
            options = {}
            )
        print 'tag:     ', tag
        print 'expected:', expected
        self.assertEquals(tag, expected)

        print 'Test 2'
        print 'Starting from position {0}; \"{1}...\"'.format(processor.i, processor.preview_segment())
        text_block = processor.next()
        expected = 'T1'
        print 'text_block:', text_block
        print 'expected:  ', expected
        self.assertEquals(text_block.text, expected)

        print 'Test 3'
        print 'Starting from position {0}; \"{1}...\"'.format(processor.i, processor.preview_segment())
        tag = processor.next()
        expected = twikitool.BaseTag(
            name = 'question',
            opening = False,
            options = {}
            )
        print 'tag:     ', tag
        print 'expected:', expected
        self.assertEquals(tag, expected)

        print 'Test 4'
        print 'Starting from position {0}; \"{1}...\"'.format(processor.i, processor.preview_segment())
        text_block = processor.next()
        expected = 'T2'
        print 'text_block:', text_block
        print 'expected:  ', expected
        self.assertEquals(text_block.text, expected)

        print 'Test 5'
        print 'Starting from position {0}; \"{1}...\"'.format(processor.i, processor.preview_segment())
        tag = processor.next()
        expected = twikitool.BaseTag(
            name = 'answer',
            opening = True,
            options = {'color' : 'red'}
            )
        print 'tag:     ', tag
        print 'expected:', expected
        self.assertEquals(tag, expected)

        print 'Test 6'
        print 'Starting from position {0}; \"{1}...\"'.format(processor.i, processor.preview_segment())
        text_block = processor.next()
        expected = 'T3'
        print 'text_block:', text_block
        print 'expected:  ', expected
        self.assertEquals(text_block.text, expected)

        print 'Test 7'
        print 'Starting from position {0}; \"{1}...\"'.format(processor.i, processor.preview_segment())
        tag = processor.next()
        expected = twikitool.BaseTag(
            name = 'answer',
            opening = False,
            options = {}
            )
        print 'tag:     ', tag
        print 'expected:', expected
        self.assertEquals(tag, expected)


    def test_ignore_literal(self):
        text = '<literal><@question>T1<@/question></literal><@answer color=red>'
        processor = twikitool.TagProcessor(text)

        print 'Test 1'
        print 'Starting from position {0}; \"{1}...\"'.format(processor.i, processor.preview_segment())
        text_block = processor.next()
        expected = '<literal><@question>T1<@/question></literal>'
        print 'text_block:', text_block
        print 'expected:  ', expected
        self.assertEquals(text_block.text, expected)

        print 'Test 2'
        print 'Starting from position {0}; \"{1}...\"'.format(processor.i, processor.preview_segment())
        tag = processor.next()
        expected = twikitool.BaseTag(
            name = 'answer',
            opening = True,
            options = {'color' : 'red'}
            )
        print 'tag:     ', tag
        print 'expected:', expected
        self.assertEquals(tag, expected)


class TestTwiki(TestCase):

    def test_basic_tag_processing(self):
        """Tests if a testtag produces expected output on a simple string"""
        text = 'bli<@testtag>T1<@/testtag>blabla'
        twiki = twikitool.Twiki()
        twiki.from_text_string(text)

        twiki.interpret()
        processed = twiki.processed_text
        expected = 'bli[TESTTAG]T1[/TESTTAG]blabla'
        self.assertEquals(processed, expected)

    def test_raises_valueerror_on_mismatch(self):
        text = '<@testtag>T1<@/othertag>'
        twiki = twikitool.Twiki()
        twiki.from_text_string(text)
        self.assertRaises(ValueError, twiki.interpret)

    def test_raises_valueerror_on_unknown_tag(self):
        text = '<@tag_blabla>T1<@/tag_blabla>'
        twiki = twikitool.Twiki()
        twiki.from_text_string(text)
        self.assertRaises(ValueError, twiki.interpret)

    def test_raises_valueerror_on_unclosed_tag(self):
        text = 'blabla<@testtag>blabla'
        twiki = twikitool.Twiki()
        twiki.from_text_string(text)
        self.assertRaises(ValueError, twiki.interpret)

    def test_input_tag_processing(self):
        """Tests if a testtag produces expected output on a simple string"""
        text = 'bli<@input file=/Users/thomas/packages/twikitool/twikitool/tests/input_test.twiki>bla'
        twiki = twikitool.Twiki()
        twiki.from_text_string(text)

        twiki.interpret()
        processed = twiki.processed_text
        expected = 'bli[TESTTAG]inputtext[/TESTTAG]bla'
        self.assertEquals(processed, expected)

