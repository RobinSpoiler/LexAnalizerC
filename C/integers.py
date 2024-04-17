"""
DOCUMENTACIÓN en página 58: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1124.pdf

integer-constant:
	decimal-constant integer-suffix(opt)
	octal-constant integer-suffix(opt)
	hexadecimal-constant integer-suffix(opt)

decimal-constant:
	nonzero-digit
	decimal-constant digit
	
octal-constant:
	0
	octal-constant octal-digit

hexadecimal-constant:
	hexadecimal-prefix hexadecimal-digit
	hexadecimal-constant hexadecimal-digit

hexadecimal-prefix: one of
	0x 0X

nonzero-digit: one of
	123456789

octal-digit: one of
	01234567

hexadecimal-digit: one of
	0123456789
	abcdef
	ABCDEF

integer-suffix:
	unsigned-suffix long-suffix(opt)
	unsigned-suffix long-long-suffix
	long-suffix unsigned-suffix(opt)
	long-long-suffix unsigned-suffix(opt)
	
unsigned-suffix: one of
	u U

long-suffix: one of
	l L

long-long-suffix: one of
	ll LL
"""

#  =================== REGEX ===================

"""
hexadecimal-prefix: one of
	0x 0X
"""
HEXADECIMAL_PREFIX_REGEX = r'(0x|0X)'


"""
nonzero-digit: one of
	123456789
"""
NONZERO_DIGIT_REGEX = r'[1-9]'

"""
octal-digit: one of
	01234567
"""
OCTAL_DIGIT_REGEX = r'[0-7]'


"""
hexadecimal-digit: one of
	0123456789
	abcdef
	ABCDEF
"""
HEXADECIMAL_DIGIT_REGEX = r'[0-9a-fA-F]'


"""
unsigned-suffix: one of
	u U
long-suffix: one of
	l L
long-long-suffix: one of
	ll LL
"""
UNSIGNED_SUFFIX_REGEX = r'(u|U)'
LONG_SUFFIX_REGEX = r'(l|L)'
LONG_LONG_SUFFIX_REGEX = r'(ll|LL)'


"""
integer-suffix:
	unsigned-suffix long-suffix(opt)				uL
	unsigned-suffix long-long-suffix				ull
	long-suffix unsigned-suffix(opt)				lU
	long-long-suffix unsigned-suffix(opt)			LLU
"""
INTEGER_SUFFIX_REGEX_L1 = r'(' + UNSIGNED_SUFFIX_REGEX + LONG_SUFFIX_REGEX  + r'?)'
INTEGER_SUFFIX_REGEX_L2 = r'(' + UNSIGNED_SUFFIX_REGEX + LONG_LONG_SUFFIX_REGEX  + r')'
INTEGER_SUFFIX_REGEX_L3 = r'(' + LONG_SUFFIX_REGEX + UNSIGNED_SUFFIX_REGEX  + r'?)'
INTEGER_SUFFIX_REGEX_L4 = r'(' + LONG_LONG_SUFFIX_REGEX + UNSIGNED_SUFFIX_REGEX  + r'?)'
# We should add L2 and L4 given that it includes the Long long suffix
INTEGER_SUFFIX_REGEX = r'((' + INTEGER_SUFFIX_REGEX_L2 + r') | (' + INTEGER_SUFFIX_REGEX_L4 + r') | (' + INTEGER_SUFFIX_REGEX_L3 + r') | (' + INTEGER_SUFFIX_REGEX_L1 + r'))'


"""
hexadecimal-constant:
	hexadecimal-prefix hexadecimal-digit			0x5
	hexadecimal-constant hexadecimal-digit			0x5Af3
"""
HEXADECIMAL_CONSTANT_REGEX = r'(' + HEXADECIMAL_PREFIX_REGEX + HEXADECIMAL_DIGIT_REGEX + r'+)'

"""
octal-constant:
	0										0
	octal-constant octal-digit				028158
"""
OCTAL_CONSTANT_REGEX = r'(0' + OCTAL_DIGIT_REGEX + r'*)'

"""
decimal-constant:
	nonzero-digit							5
	decimal-constant digit					5913052
"""
DECIMAL_CONSTANT_REGEX = r'(' + NONZERO_DIGIT_REGEX  + r'\d*)'


"""
integer-constant:
	decimal-constant integer-suffix(opt)			5913052ull
	octal-constant integer-suffix(opt)				028158lU
	hexadecimal-constant integer-suffix(opt)		0x5Af3LLU
"""
INTEGER_CONSTANT_REGEX = r'((' + HEXADECIMAL_CONSTANT_REGEX + INTEGER_SUFFIX_REGEX + r'?) | (' + DECIMAL_CONSTANT_REGEX + INTEGER_SUFFIX_REGEX + r'?) | (' + OCTAL_CONSTANT_REGEX + INTEGER_SUFFIX_REGEX + r'?))'
