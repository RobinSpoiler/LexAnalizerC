"""
https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1124.pdf
Documentación en sección 6.4.4.2: Floating constants

floating-constant:
	decimal-floating-constant
	hexadecimal-floating-constant

decimal-floating-constant:
	fractional-constant exponent-partopt floating-suffixopt
	digit-sequence exponent-part floating-suffixopt

hexadecimal-floating-constant:
	hexadecimal-prefix hexadecimal-fractional-constant binary-exponent-part floating-suffixopt
	hexadecimal-prefix hexadecimal-digit-sequence binary-exponent-part floating-suffixopt

fractional-constant:
	digit-sequenceopt . digit-sequence
	digit-sequence .

exponent-part:
e signopt digit-sequence
E signopt digit-sequence

sign: one of
	+ -

digit-sequence:
	digit
	digit-sequence digit

hexadecimal-fractional-constant:
	hexadecimal-digit-sequence(opt) . hexadecimal-digit-sequence
	hexadecimal-digit-sequence .

binary-exponent-part:
	p sign(opt) digit-sequence
	P sign(opt) digit-sequence

hexadecimal-digit-sequence:
	hexadecimal-digit
	hexadecimal-digit-sequence hexadecimal-digit

floating-suffix: one of
	flFL

"""

from integers import HEXADECIMAL_PREFIX_REGEX

# =========== REGEX ============

"""
sign: one of
	+ -
"""
SIGN_REGEX = r'(\+|-)'

"""
digit-sequence:
	digit
	digit-sequence digit
"""
DIGIT_SEQUENCE_REGEX = r'[0-9]+'
HEXADECIMAL_SEQUENCE_REGEX = r'[0-9a-fA-F]+'

"""
floating-suffix: one of
	f l F L
"""
FLOATING_SUFFIX_REGEX = r'(f|l|F|L)'

"""
exponent-part:
e sign(opt) digit-sequence		e+582
E sign(opt) digit-sequence		E-491
"""
EXPONENT_PART_REGEX = r'((e|E)' + SIGN_REGEX + r'?' + DIGIT_SEQUENCE_REGEX + r')'

"""
binary-exponent-part:
	p sign(opt) digit-sequence		p+59
	P sign(opt) digit-sequence		P-13
"""
BINARY_EXPONENT_PART_REGEX = r'((p|P)' + SIGN_REGEX + r'?' + DIGIT_SEQUENCE_REGEX + r')'

"""
hexadecimal-fractional-constant:
	hexadecimal-digit-sequence(opt) . hexadecimal-digit-sequence 		.A52D
	hexadecimal-digit-sequence .										58BF32
"""
HEXADECIMAL_FRACTIONAL_CONSTANT_L1 = r'((' + HEXADECIMAL_SEQUENCE_REGEX + r')?\.' + HEXADECIMAL_SEQUENCE_REGEX + r')'
HEXADECIMAL_FRACTIONAL_CONSTANT_L2 = r'(' + HEXADECIMAL_SEQUENCE_REGEX + r'\.)'
HEXADECIMAL_FRACTIONAL_CONSTANT_REGEX = r'((' + HEXADECIMAL_FRACTIONAL_CONSTANT_L1 + r') | (' + HEXADECIMAL_FRACTIONAL_CONSTANT_L2 + r'))'


"""
fractional-constant:
	digit-sequence(opt) . digit-sequence		.4920
	digit-sequence .							3420.
"""
FRACTIONAL_CONSTANT_L1 = r'((' + DIGIT_SEQUENCE_REGEX + r')?\.' + DIGIT_SEQUENCE_REGEX + r')'
FRACTIONAL_CONSTANT_L2 = r'(' + DIGIT_SEQUENCE_REGEX + r'\.)'
FRACTIONAL_CONSTANT_REGEX = r'(' + FRACTIONAL_CONSTANT_L1 + r'|' + FRACTIONAL_CONSTANT_L2 + r')'


"""
hexadecimal-floating-constant:
	hexadecimal-prefix hexadecimal-fractional-constant binary-exponent-part floating-suffix(opt)
		0X					   .A52D						 p+59                f
	hexadecimal-prefix hexadecimal-digit-sequence binary-exponent-part floating-suffix(opt)
		0x						4F204B						P-13				L
"""
HEXADECIMAL_FLOATING_L1 = r'(' + HEXADECIMAL_PREFIX_REGEX + HEXADECIMAL_FRACTIONAL_CONSTANT_REGEX + BINARY_EXPONENT_PART_REGEX + FLOATING_SUFFIX_REGEX + r'?)'
HEXADECIMAL_FLOATING_L2 = r'(' + HEXADECIMAL_PREFIX_REGEX + HEXADECIMAL_SEQUENCE_REGEX + BINARY_EXPONENT_PART_REGEX + FLOATING_SUFFIX_REGEX + '?)'
HEXADECIMAL_FLOATING_CONSTANT = r'(' + HEXADECIMAL_FLOATING_L1 + r'|' + HEXADECIMAL_FLOATING_L2 + r')'


"""
decimal-floating-constant:
	fractional-constant exponent-part(opt) floating-suffix(opt)   .4920e+582F
	digit-sequence exponent-part floating-suffix(opt)			   4810E-491l
"""
DECIMAL_FLOATING_L1 = r'(' + FRACTIONAL_CONSTANT_REGEX + EXPONENT_PART_REGEX + r'?' + FLOATING_SUFFIX_REGEX + r'?)'
DECIMAL_FLOATING_L2 = r'(' + DIGIT_SEQUENCE_REGEX + EXPONENT_PART_REGEX + FLOATING_SUFFIX_REGEX + r'?)'
DECIMAL_FLOATING_CONSTANT = r'(' + DECIMAL_FLOATING_L1 + r'|' + DECIMAL_FLOATING_L2 + r')'

"""
floating-constant:
	decimal-floating-constant			.4920e+582F	
	hexadecimal-floating-constant      0x4F204BP-13L
"""
FLOATING_CONSTANT_REGEX = r'(' + DECIMAL_FLOATING_CONSTANT + r'|' + HEXADECIMAL_FLOATING_CONSTANT + r')'