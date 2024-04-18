"""
Section 6.4.7: HEADER NAMES
https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1124.pdf

header-name:
	< h-char-sequence >
	" q-char-sequence "
h-char-sequence:
	h-char
	h-char-sequence h-char
h-char:
	any member of the source character set except
	the new-line character and >
q-char-sequence:
	q-char
	q-char-sequence q-char
q-char:
	any member of the source character set except
	the new-line character and "
"""

Q_CHAR = r'([^\n"])'
Q_CHAR_SEQUENCE = r'(' + Q_CHAR + r'+)'

H_CHAR = r'([^\n>])'
H_CHAR_SEQUENCE = r'(' + H_CHAR + r'+)'

H_CHAR_HEADER = r'(<' + H_CHAR_SEQUENCE + r'>)'
Q_CHAR_HEADER = r'("' + Q_CHAR_SEQUENCE + r'")'
HEADER_NAME_REGEX = r'(\#include\s(' + H_CHAR_HEADER + r'|' + Q_CHAR_HEADER + r'))'
