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
        
# class TestFloats(unittest.TestCase):
#     def setUp(self):
#         self.lexer = lexer.getLexer()

#     def test_basic_decimal_floats(self):
#         self.lexer.input('0. 72.40 072.30 2.71828 .25')
#         for value in [0.0, 72.4, 72.3, 2.71828, .25]:
#             token = self.lexer.token()
#             self.assertAlmostEqual(token.value, value)
#             self.assertEqual(token.type, 'FLOAT')

#     def test_basic_decimal_floats_sci_notation(self):
#         self.lexer.input('1.e+0 6.67428e-11 1E6 .12345E+5')
#         for value in [1.0, 6.67428e-11, 1e6, 0.12345E+5]:
#             token = self.lexer.token()
#             self.assertAlmostEqual(token.value, value)
#             self.assertEqual(token.type, 'FLOAT')
    
#     def test_decimal_underscored_floats(self):
#         self.lexer.input('1_5. 0.15e+0_2')
#         for value in [15.0, 15.0]:
#             token = self.lexer.token()
#             self.assertAlmostEqual(token.value, value)
#             self.assertEqual(token.type, 'FLOAT')

#     def test_wrong_floats_1(self):
#         self.lexer.input('1_.5')
#         self.lexer.token()  # consumes "1"
#         self.assertRaises(lex.LexError, self.lexer.token)

#     def test_wrong_floats_2(self):
#         self.lexer.input('1._5')
#         self.lexer.token()  # consumes "1."
#         self.assertRaises(lex.LexError, self.lexer.token)

#     def test_wrong_floats_3(self):
#         self.lexer.input('1.5_e1')
#         self.lexer.token()  # consumes "1.5"
#         self.assertRaises(lex.LexError, self.lexer.token)

#     def test_wrong_floats_4(self):
#         self.lexer.input('1.5e_1')
#         self.lexer.token()
#         self.assertRaises(lex.LexError, self.lexer.token)

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