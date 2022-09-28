# Functions that can generate attribute values.
#
# These are functions that can be used in the GenerateFuncAttribute() class
# (see module generator.py). They generate values according to some internal
# functionality.
#
# The requirement of any such functions are:
# 1) that it must return a string
# 2) it can have been 0 and 5 parameters
#
#
# Examples of such functions are:
# - American telephone numbers
# - Date of Birth (DOB)
# - US social security numbers
# - Credit Card Number
# etc.

# Peter Christen and Dinusha Vatsalan, January-March 2012
# Modified by Sepideh Mosaferi 05/30/2017
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

import random
import string
import numpy
import datetime

import basefunctions

# -----------------------------------------------------------------------------
#


def generate_phone_number_ethiopia():
    """Randomly generate an American telephone number made of a three-digit area
       code and a three-digit and a four-digit numbers (with a "-" between).
       For example: '301-433-2170'
       For details see: https://en.wikipedia.org/wiki/Telephone_numbers_in_the_Ethiopia
    """

    area_code = random.choice(['011-111', '011-112', '011-114',
                               '011-2', '011-3', '011-4', '011-5', '011-651', '011-652', '011-654', '011-655',
                               '022-',  '025-',
                               '033-',  '034-',
                               '046-',  '047-',
                               '057-',  '058-',
                               '091-1', '091-4', '091-6', '091-7', '091-8',
                               '098-111', '098-119'])

    number1 = random.randint(1, 999)
    number2 = random.randint(1, 9999)
    number = 'xxx-' + str(number1).zfill(3)+'-'+str(number2).zfill(4)

    phone_str = area_code + number[len(area_code):]

    assert len(phone_str) == 12

    return phone_str

# -----------------------------------------------------------------------------
#


def generate_date_of_birth(mu, sigma):
    """Randomly generate a dob made of two two-digit numbers and one
       four digit number (with a "/" between each number group).
       For example: '29/01/1990' 'day/month/year'
    """

    age_years = int(random.gauss(mu, sigma))
    if age_years > 80:
        age_years = 80
    if age_years < 1:
        age_years = 1
    year = 2020 - age_years
    start_date = datetime.date(year, 1, 1)
    date = start_date + datetime.timedelta(random.randint(1, 365))
    cc_str = date.strftime("%Y%m%d")
    return cc_str

# -----------------------------------------------------------------------------
#


def generate_national_id_number():
    """Randomly generate a national ID number
    """

    number1 = generate_date_of_birth(20, 5)
    number2 = random.randint(1, 9999)
    number3 = random.randint(1, 99)
    number4 = random.randint(1, 9)
    cc_str = number1 + str(number2).zfill(4)+str(number3).zfill(2)+str(number4)

    assert len(cc_str) == 15

    return cc_str

# -----------------------------------------------------------------------------
#


def generate_client_registration_facility_code():
    """
    """

    cc_str = random.choice(['AAAA', 'BBBB', 'CCCC'])

    assert len(cc_str) == 4

    return cc_str

# -----------------------------------------------------------------------------
#


def generate_client_registration_id():
    """Randomly generate a national ID number
    123412345678
    AAAAdddddddd
    AAAA85322047
    """

    code = generate_client_registration_facility_code()

#                               12345678
    number1 = random.randint(1, 99999999)
    cc_str = code+str(number1).zfill(8)

    assert len(cc_str) == 12

    return cc_str

# -----------------------------------------------------------------------------
#


def generate_social_security_number():
    """Randomly generate a SSN made of one three-digit numbers and one
       two-digit numbers and one four-digit numbers (with a "-" between each number group).
       The SSN is nine-digit number in the format "AAA-GG-SSSS".
       For more information see
       https://en.wikipedia.org/wiki/Social_Security_number and
       https://en.wikipedia.org/wiki/List_of_Social_Security_Area_Numbers
    """

    number1 = random.randint(1, 728)
    assert number1 > 0

    number2 = random.randint(1, 99)
    assert number2 > 0

    number3 = random.randint(1, 9999)
    assert number3 > 0

    cc_str = str(number1).zfill(3)+'-'+str(number2).zfill(2)+'-' + \
        str(number3).zfill(4)

    assert len(cc_str) == 11

    return cc_str

# -----------------------------------------------------------------------------
#


def generate_enrollment_hiv_id():
    """
    """

    char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
    aa = ''.join(random.choice(char_set) for _ in range(2))
    bb = ''.join(random.choice(char_set) for _ in range(2))
    ccc = ''.join(random.choice(char_set) for _ in range(3))
    ddddd = ''.join(random.choice(char_set) for _ in range(5))

    cc_str = aa+'/'+bb+'/'+ccc+'/'+ddddd

    assert len(cc_str) == 15

    return cc_str

# -----------------------------------------------------------------------------
#


def generate_enrollment_hiv_facility_code():
    """

    """

    char_set = string.digits
    cc_str = ''.join(random.choice(char_set) for _ in range(6))

    assert len(cc_str) == 6

    return cc_str

# -----------------------------------------------------------------------------
#


def generate_unique_art_number():
    """Randomly generate a UAN - Unique ART Number
    The enrollment ID is known as a Unique ART Number (UAN) and should be globally unique.
    12 digits code or alphanumeric string such as 'AA/BB/CCC/DDDDD' where
    AA -> region
    BB -> facility type
    CCC -> facility code
    DDDDD -> sequential ART patient ID at the facilitymade of one three-digit numbers and one
    For more information see
    https://google.com
    """

    char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
    aa = ''.join(random.choice(char_set) for _ in range(2))
    bb = ''.join(random.choice(char_set) for _ in range(2))
    ccc = ''.join(random.choice(char_set) for _ in range(3))
    ddddd = ''.join(random.choice(char_set) for _ in range(5))

    cc_str = aa+'/'+bb+'/'+ccc+'/'+ddddd

    assert len(cc_str) == 15

    return cc_str

# -----------------------------------------------------------------------------
#


def generate_medical_record_number():
    """Randomly generate a MRN - Medical Record Number
    A Facility registration number is a six digit number called a Medical
    Record Number (MRN), this is unique per facility but not globally unique
    For more information see
    https://google.com
    """

    char_set = string.digits
    cc_str = ''.join(random.choice(char_set) for _ in range(6))

    assert len(cc_str) == 6

    return cc_str

# -----------------------------------------------------------------------------
#


def generate_credit_card_number():
    """Randomly generate a credit card made of four four-digit numbers (with a
       space between each number group). For example: '1234 5678 9012 3456'

       For details see: http://en.wikipedia.org/wiki/Bank_card_number
    """

    number1 = random.randint(1, 9999)
    assert number1 > 0

    number2 = random.randint(1, 9999)
    assert number2 > 0

    number3 = random.randint(1, 9999)
    assert number3 > 0

    number4 = random.randint(1, 9999)
    assert number4 > 0

    cc_str = str(number1).zfill(4)+' '+str(number2).zfill(4)+' ' + \
        str(number3).zfill(4)+' '+str(number4).zfill(4)

    assert len(cc_str) == 19

    return cc_str

# -----------------------------------------------------------------------------
#


def generate_uniform_value(min_val, max_val, val_type):
    """Randomly generate a numerical value according to a uniform distribution
       between the minimum and maximum values given.

       The value type can be set as 'int', so a string formatted as an integer
       value is returned; or as 'float1' to 'float9', in which case a string
       formatted as floating-point value with the specified number of digits
       behind the comma is returned.

       Note that for certain situations and string formats a value outside the
       set range might be returned. For example, if min_val=100.25 and
       val_type='float1' the rounding can result in a string value '100.2' to
       be returned.

       Suitable minimum and maximum values need to be selected to prevent such
       a situation.
    """

    basefunctions.check_is_number('min_val', min_val)
    basefunctions.check_is_number('max_val', max_val)
    assert min_val < max_val

    r = random.uniform(min_val, max_val)

    return basefunctions.float_to_str(r, val_type)

# -----------------------------------------------------------------------------


def generate_normal_value(mu, sigma, min_val, max_val, val_type):
    """Randomly generate a numerical value according to a normal distribution
       with the mean (mu) and standard deviation (sigma) given.

       A minimum and maximum allowed value can given as additional parameters,
       if set to None then no minimum and/or maximum limit is set.

       The value type can be set as 'int', so a string formatted as an integer
       value is returned; or as 'float1' to 'float9', in which case a string
       formatted as floating-point value with the specified number of digits
       behind the comma is returned.
    """

    basefunctions.check_is_number('mu', mu)
    basefunctions.check_is_number('sigma', sigma)
    assert sigma > 0.0

    if (min_val != None):
        basefunctions.check_is_number('min_val', min_val)
        assert min_val <= mu

    if (max_val != None):
        basefunctions.check_is_number('max_val', max_val)
        assert max_val >= mu

    if ((min_val != None) and (max_val != None)):
        assert min_val < max_val

    if (min_val != None) or (max_val != None):
        in_range = False  # For testing if the random value is with the range
    else:
        in_range = True

    r = random.normalvariate(mu, sigma)

    while (in_range == False):
        if ((min_val == None) or ((min_val != None) and (r >= min_val))):
            in_range = True

        if ((max_val != None) and (r > max_val)):
            in_range = False

        if (in_range == True):
            r_str = basefunctions.float_to_str(r, val_type)
            r_test = float(r_str)
            if (min_val != None) and (r_test < min_val):
                in_range = False
            if (max_val != None) and (r_test > max_val):
                in_range = False

        if (in_range == False):
            r = random.normalvariate(mu, sigma)

    if (min_val != None):
        assert r >= min_val
    if (max_val != None):
        assert r <= max_val

    return basefunctions.float_to_str(r, val_type)


# =============================================================================

# If called from command line perform some examples: Generate values
#
if (__name__ == '__main__'):

    num_test = 20

    print('Generate %d Ethiopian telephone numbers:' % (num_test))
    for i in range(num_test):
        print(' ', generate_phone_number_ethiopia())
    print

    print('Generate %d date of births:' % (num_test))
    for i in range(num_test):
        print(' ', generate_date_of_birth())
    print

    print('Generate %d social security number:' % (num_test))
    for i in range(num_test):
        print(' ', generate_social_security_number())
    print

    print('Generate %d credit card numbers:' % (num_test))
    for i in range(num_test):
        print(' ', generate_credit_card_number())
    print

    print('Generate %d uniformly distributed integer numbers between -100' %
          (num_test) + ' and -5:')
    for i in range(num_test):
        print(' ', generate_uniform_value(-100, -5, 'int'))
    print

    print('Generate %d uniformly distributed floating-point numbers with ' %
          (num_test) + '3 digits between -55 and 55:')
    for i in range(num_test):
        print(' ', generate_uniform_value(-55, 55, 'float3'))
    print

    print('Generate %d uniformly distributed floating-point numbers with ' %
          (num_test) + '7 digits between 147 and 9843:')
    for i in range(num_test):
        print(' ', generate_uniform_value(147, 9843, 'float7'))
    print

    print('Generate %d normally distributed integer numbers between -200' %
          (num_test) + ' and -3 with mean -50 and standard deviation 44:')
    for i in range(num_test):
        print(' ', generate_normal_value(-50, 44, -200, -3, 'int'))
    print

    print('Generate %d normally distributed floating-point numbers with ' %
          (num_test) + '5 digits between -100 and 100 and with mean 22 and ' +
          'standard deviation 74:')
    for i in range(num_test):
        print(' ', generate_normal_value(22, 74, -100, 100, 'float5'))
    print

    print('Generate %d normally distributed floating-point numbers with ' %
          (num_test) + '9 digits with mean 22 and standard deviation 74:')
    for i in range(num_test):
        print(' ', generate_normal_value(22, 74, min_val=None, max_val=None,
                                         val_type='float9'))
    print

    print('Generate %d normally distributed floating-point numbers with ' %
          (num_test) + '2 digits with mean 22 and standard deviation 24 that' +
          ' are larger than 10:')
    for i in range(num_test):
        print(' ', generate_normal_value(22, 74, min_val=10, max_val=None,
                                         val_type='float2'))
    print

    print('Generate %d normally distributed floating-point numbers with ' %
          (num_test) + '4 digits with mean 22 and standard deviation 24 that' +
          ' are smaller than 30:')
    for i in range(num_test):
        print(' ', generate_normal_value(22, 74, min_val=None, max_val=40,
                                         val_type='float4'))
    print
