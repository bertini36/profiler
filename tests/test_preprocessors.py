# -*- coding: UTF-8 -*-

import pytest

from src.classes.preprocessors import MyPreprocessor


@pytest.mark.unit
class TestMyPreprocessor:
    @classmethod
    def setup_class(cls):
        cls.preprocessor = MyPreprocessor(None)

    def test_fix_strange_quotes(self):
        result = self.preprocessor.fix_strange_quotes('‘`❞❯')
        assert result == '\'\'""'

    def test_no_fix_strange_quotes(self):
        result = self.preprocessor.fix_strange_quotes('\'\'""')
        assert result == '\'\'""'

    def test_normalize_whitespace(self):
        result = self.preprocessor.normalize_whitespace('ouh   \n\n\nmama')
        assert result == 'ouh mama'

    def test_no_normalize_whitespace(self):
        result = self.preprocessor.normalize_whitespace('ouh mama')
        assert result == 'ouh mama'

    def test_replace_urls(self):
        result = self.preprocessor.replace_urls('www.albertopou.herokuapp.com')
        assert result == '<URL>'

    def test_no_replace_urls(self):
        result = self.preprocessor.replace_urls('let\'s go')
        assert result == 'let\'s go'

    def test_replace_mentions(self):
        result = self.preprocessor.replace_mentions('@joanfont')
        assert result == '<MENTION>'

    def test_no_replace_mentions(self):
        result = self.preprocessor.replace_mentions('joanfont')
        assert result == 'joanfont'

    def test_replace_emails(self):
        result = self.preprocessor.replace_emails('test@test.com')
        assert result == '<EMAIL>'

    def test_no_replace_emails(self):
        result = self.preprocessor.replace_emails('test')
        assert result == 'test'

    def test_replace_numbers(self):
        result = self.preprocessor.replace_numbers('34')
        assert result == '<NUMBER>'

    def test_no_replace_numbers(self):
        result = self.preprocessor.replace_numbers('test')
        assert result == 'test'

    def test_replace_digits(self):
        result = self.preprocessor.replace_digits('1,1')
        assert result == '0,0'

    def test_no_replace_digits(self):
        result = self.preprocessor.replace_digits('test')
        assert result == 'test'

    def test_replace_currencies(self):
        result = self.preprocessor.replace_currencies('€')
        assert result == '<CURRENCY>'

    def test_no_replace_currencies(self):
        result = self.preprocessor.replace_currencies('test')
        assert result == 'test'

    def test_replace_emojis(self):
        result = self.preprocessor.replace_emojis('😀')
        assert result == '<EMOJI>'

    def test_no_replace_emojis(self):
        result = self.preprocessor.replace_emojis(':)')
        assert result == ':)'

    def test_remove_punct(self):
        result = self.preprocessor.remove_punct('...')
        assert result == '   '

    def test_no_remove_punct(self):
        result = self.preprocessor.remove_punct('test')
        assert result == 'test'

    def test_remove_multiple_spaces(self):
        result = self.preprocessor.remove_multiple_spaces('   ')
        assert result == ' '

    def test_no_remove_multiple_spaces(self):
        result = self.preprocessor.remove_multiple_spaces(' ')
        assert result == ' '

    def test_get_spanish_stopwords(self):
        text = 'hola don Pepito que tal está'
        stopwords = self.preprocessor.get_stopwords(text)
        assert 'nosotras' in stopwords

    def test_get_no_spanish_stopwords(self):
        text = 'hello how are you'
        stopwords = self.preprocessor.get_stopwords(text)
        assert 'nosotras' not in stopwords

    def test_filter_stopwords(self):
        text = 'la casa azul'
        filtered_text = self.preprocessor.filter_stopwords(text)
        assert filtered_text == 'casa azul'

    def test_no_filter_stopwords(self):
        text = 'casa azul'
        filtered_text = self.preprocessor.filter_stopwords(text)
        assert filtered_text == 'casa azul'
