import math
from typing import List, Union

decimal_separator = '.'
positive_suffixes: List[Union[str, List[str]]] = ['', ['k', 'K'], 'M', 'G', 'T', 'P']
negative_suffixes: List[Union[str, List[str]]] = ['m', 'u', 'n', 'p']


def ends_with_suffix(number_str: str, suffixes: Union[str, List[str]]) -> bool:
    if isinstance(suffixes, str):
        suffixes = [suffixes]
    for suffix in suffixes:
        if number_str.endswith(suffix):
            return True
    return False


def get_suffix_from_number(number: float) -> str:
    suffixes = positive_suffixes + negative_suffixes[::-1]
    if number == 0:
        return ''
    magnitude = int(math.floor(math.log(abs(number), 1e3)))
    if magnitude <= len(positive_suffixes) - 1 and magnitude >= -len(negative_suffixes):
        return get_suffix_from_options(suffixes[magnitude])
    return ''


def get_suffix_from_options(suffix_options: Union[str, List[str]]) -> str:
    if isinstance(suffix_options, str):
        return suffix_options
    return suffix_options[0]


def format(number: complex, unit='', decimal: int = 2) -> str:
    if isinstance(number, complex):
        return format_complex(number, unit, decimal)
    return format_float(number, unit, decimal)


def format_float(number: float, unit='', decimal: int = 2) -> str:
    suffixes = positive_suffixes + negative_suffixes[::-1]
    if number == 0:
        return '0' + unit
    magnitude = int(math.floor(math.log(abs(number), 1e3)))
    if magnitude <= len(positive_suffixes) - 1 and magnitude >= -len(negative_suffixes):
        number_str = f'{number/1e3**magnitude:.{decimal}f}'
        number_str = number_str.strip('0').strip('.')
        suffix_options = suffixes[magnitude]
        suffix = suffix_options if isinstance(suffix_options, str) else suffix_options[0]
        number_str = f'{number_str}{suffix}{unit}'
    else:
        number_str = f'{number:.{decimal}e}{unit}'
    return number_str.replace('.', decimal_separator)


def format_complex(number: complex, unit: str = '', decimal: int = 2) -> str:
    if number.imag == 0:
        return format(number.real, unit, decimal)
    if number.real == 0:
        if number.imag >= 0:
            return 'j' + format(number.imag, unit, decimal)
        else:
            return '-j' + format(-number.imag, unit, decimal)
    real = format(number.real, '', decimal)
    imag = format(number.imag, '', decimal)
    real_suffix = get_suffix_from_number(number.real)
    imag_suffix = get_suffix_from_number(number.imag)
    if real_suffix == imag_suffix:
        real = real.replace(real_suffix, '')
        imag = imag.replace(imag_suffix, '')
        return f'({real} + {imag}j){real_suffix}{unit}'
    return f'({real} + {imag}j){unit}'


def revert(number_str: str, unit: str = '') -> float:
    suffixes = positive_suffixes + negative_suffixes[::-1]
    number_str = number_str.replace(decimal_separator, '.')
    number_str = number_str.replace(' ', '')
    if len(unit) > 0 and number_str.endswith(unit):
        number_str = number_str[:-len(unit)]
    for i, suffix_options in enumerate(suffixes):
        if ends_with_suffix(number_str, suffix_options):
            sorted_sufixes = negative_suffixes[::-1] + positive_suffixes
            magnitude = sorted_sufixes.index(suffix_options) - len(negative_suffixes)
            if magnitude != 0:
                return float(number_str[:-len(get_suffix_from_options(suffix_options))]) * 1e3**magnitude
    return float(number_str)
