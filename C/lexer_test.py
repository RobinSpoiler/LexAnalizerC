import unittest
import ply.lex as lex
import lexer

class TestKeywords(unittest.TestCase):
    def setUp(self):
        self.lexer = lexer.getLexer()

    def test_basic_keywords(self):
        self.lexer.input('break auto while for')
        for value in ["break", "auto", "while", "for"]:
            token = self.lexer.token()
            self.assertAlmostEqual(token.value, value)
            self.assertEqual(token.type, 'KEYWORD')

class TestPunctuators(unittest.TestCase):
    def setUp(self):
        self.lexer = lexer.getLexer()
    
    def test_basic_punctuators(self):
        self.lexer.input(': << -> + ;')
        for value in [":", "<<", "->", "+", ";"]:
            token = self.lexer.token()
            self.assertAlmostEqual(token.value, value)
            self.assertEqual(token.type, 'PUNCTUATOR')


class TestIntegers(unittest.TestCase):
    def setUp(self):
        self.lexer = lexer.getLexer()
    
    def test_decimal_constant(self):
        self.lexer.input('5913052ull')
        token = self.lexer.token()
        self.assertEqual(token.type, 'INT')
        self.assertEqual(token.value, '5913052ull')

    def test_octal_constant(self):
        self.lexer.input('027153lU')
        token = self.lexer.token()
        self.assertEqual(token.type, 'INT')
        self.assertEqual(token.value, '027153lU')

    def test_hexadecimal_constant(self):
        self.lexer.input('0x5Af3LLU') 
        token = self.lexer.token()
        self.assertEqual(token.value, '0x5Af3LLU')
        self.assertEqual(token.type, 'INT')
        
class TestFloats(unittest.TestCase):
    def setUp(self):
        self.lexer = lexer.getLexer()

    def test_decimal_fractional(self):
        self.lexer.input('1.52 5. .569')
        for value in ['1.52', '5.', '.569']:
            token = self.lexer.token()
            self.assertEqual(token.type, 'FLOAT')
            self.assertEqual(token.value, value)

    def test_hexadecimal_floating_constant(self):
        self.lexer.input('0X.A52Dp+59f 0x4F204BP-13L')
        for value in ['0X.A52Dp+59f', '0x4F204BP-13L']:
            token = self.lexer.token()
            self.assertEqual(token.type, 'FLOAT')
            self.assertEqual(token.value, value)

    def test_decimal_floating_constant(self):
        self.lexer.input('.4920e+582F 4810E-491l')
        for value in ['.4920e+582F', '4810E-491l']:
            token = self.lexer.token()
            self.assertEqual(token.type, 'FLOAT')
            self.assertEqual(token.value, value)

class TestStrings(unittest.TestCase):
    def setUp(self):
        self.lexer = lexer.getLexer()

    def test_basic_strings(self):
        self.lexer.input("'Le petit prince'")
        token = self.lexer.token()
        self.assertEqual(token.type, 'STR')
        self.assertEqual(token.value, "'Le petit prince'")

    def test_basic_strings_2(self):
        self.lexer.input('"Hola \\\"%s\\\""')
        token = self.lexer.token()
        self.assertEqual(token.type, 'STR')
        self.assertEqual(token.value, '"Hola \\\"%s\\\""')

if __name__ == '__main__':
    unittest.main()