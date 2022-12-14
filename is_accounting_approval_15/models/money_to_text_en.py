# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging


_logger = logging.getLogger(__name__)

# -------------------------------------------------------------
# ENGLISH
# -------------------------------------------------------------

to_19 = ('Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six',
         'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen',
         'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen')
tens = ('Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety')
denom = ('',
         'Thousand', 'Million', 'Billion', 'Trillion', 'Quadrillion',
         'Quintillion', 'Sextillion', 'Septillion', 'Octillion', 'Nonillion',
         'Decillion', 'Undecillion', 'Duodecillion', 'Tredecillion', 'Quattuordecillion',
         'Sexdecillion', 'Septendecillion', 'Octodecillion', 'Novemdecillion', 'Vigintillion')

def _get_currency_name_by_code(cur):
    result={'SDG':['Pound','Piastres','Piastre'],
            'AED':['Dirham','Fils','Fils'],
            'CFA':['Franc','Cents','Cent'],
            'EGP':['Pound','Piastres','Piastre'],
            'EUR':['Euro','Cents','Cent'],
            'USD':['Dollar','Cents','Cent'],
            'SSP':['Pound','Piastres','Piastre'],
            'SAR':['Riyal','Hallals','halalas']
            }
    return result[cur.upper()]


def _convert_nn(val):
    """convert a value < 100 to English.
    """
    if val < 20:
        return to_19[val]
    for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens)):
        if dval + 10 > val:
            if val % 10:
                return dcap + '-' + to_19[val % 10]
            return dcap


def _convert_nnn(val):
    """
        convert a value < 1000 to english, special cased because it is the level that kicks
        off the < 100 special case.  The rest are more general.  This also allows you to
        get strings in the form of 'forty-five hundred' if called directly.
    """
    word = ''
    (mod, rem) = (val % 100, val // 100)
    if rem > 0:
        word = to_19[rem] + ' Hundred'
        if mod > 0:
            word += ' '
    if mod > 0:
        word += _convert_nn(mod)
    return word


def english_number(val):
    if val < 100:
        return _convert_nn(val)
    if val < 1000:
        return _convert_nnn(val)
    for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom))):
        if dval > val:
            mod = 1000 ** didx
            l = val // mod
            r = val - (l * mod)
            ret = _convert_nnn(l) + ' ' + denom[didx]
            if r > 0:
                ret = ret + ', ' + english_number(r)
            return ret


def amount_to_text(number, currency):
    number = '%.2f' % number
    units_name = _get_currency_name_by_code(currency)[0]
    list = str(number).split('.')
    start_word = english_number(int(list[0]))
    end_word = english_number(int(list[1]))
    cents_number = int(list[1])
    cents_name = (cents_number > 1) and _get_currency_name_by_code(currency)[1] or _get_currency_name_by_code(currency)[2]
    # return ' '.join(filter(None,
    #                        [start_word, units_name, (start_word or units_name) and (end_word or cents_name) and 'and',
    #                         end_word, cents_name]))

    if start_word and end_word != "Zero":
        final_result = start_word+' '+_get_currency_name_by_code(currency)[0]+' '+'and'+' '+end_word+" "+cents_name
    if start_word and end_word == "Zero":
        final_result = ''
    if start_word != "Zero" and end_word == "Zero":
        final_result = start_word + ' ' + _get_currency_name_by_code(currency)[0]
    if start_word == "Zero" and end_word != "Zero":
        final_result = end_word + " " + cents_name
    return final_result

