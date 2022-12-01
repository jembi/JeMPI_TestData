import codecs
import random
from collections.abc import Generator


def position_mod_normal(in_str):
    """Select any position in the given input string with normally distributed
       likelihood where the average of the normal distribution is set to one
       character behind the middle of the string, and the standard deviation is
       set to 1/4 of the string length.

       This is based on studies on the distribution of errors in real text which
       showed that errors such as typographical mistakes are more likely to
       appear towards the middle and end of a string but not at the beginning.

       Return 0 is the string is empty.
    """

    if (in_str == ''):  # Empty input string
        return 0

    str_len = len(in_str)

    mid_pos = str_len / 2.0 + 1
    std_dev = str_len / 4.0
    max_pos = str_len - 1

    pos = int(round(random.gauss(mid_pos, std_dev)))
    while ((pos < 0) or (pos > max_pos)):
        pos = int(round(random.gauss(mid_pos, std_dev)))

    return pos


def all_upper_case_corruptor() -> Generator[None]:
    y = None
    while True:
        meta = yield y
        value = meta
        y = value.upper()


def missing_value_corruptor() -> Generator[None]:
    while True:
        yield None


def str2comma_separated_list(s):
    in_list = s.split(',')
    out_list = []
    for e in in_list:
        e = e.strip()
        if ((e.startswith('"') and e.endswith('"')) or
                (e.startswith("'") and e.endswith("'"))):
            e = e[1:-1]  # Remove quotes
        out_list.append(e)
    return out_list


def read_csv_file(file_name, encoding, header_line):
    in_file = codecs.open(file_name, encoding='ascii')
    if header_line:
        header_line = in_file.readline()
        header_list = str2comma_separated_list(header_line)
    else:
        header_list = None
    file_data = []
    for line_str in in_file:
        line_str = line_str.strip()
        if (line_str.startswith('#') == False) and (line_str != ''):
            line_list = str2comma_separated_list(line_str)
            file_data.append(line_list)
    in_file.close()
    return header_list, file_data


def position_mod_normal(in_str):
    if in_str == '':  # Empty input string
        return 0
    str_len = len(in_str)
    mid_pos = str_len / 2.0 + 1
    std_dev = str_len / 4.0
    max_pos = str_len - 1
    pos = int(round(random.gauss(mid_pos, std_dev)))
    while (pos < 0) or (pos > max_pos):
        pos = int(round(random.gauss(mid_pos, std_dev)))
    return pos


def ocr_corruptor() -> Generator[None]:
    lookup_file_name = 'metadata/ocr-variations.csv'
    has_header_line = None
    unicode_encoding = None
    ocr_val_dict = {}  # The dictionary to hold the OCR variations
    position_function = position_mod_normal
    header_list, lookup_file_data = read_csv_file(lookup_file_name, unicode_encoding, has_header_line)
    for rec_list in lookup_file_data:
        org_val = rec_list[0].strip()
        var_val = rec_list[1].strip()
        this_org_val_list = ocr_val_dict.get(org_val, [])
        this_org_val_list.append(var_val)
        ocr_val_dict[org_val] = this_org_val_list
        this_org_val_list = ocr_val_dict.get(var_val, [])
        this_org_val_list.append(org_val)
        ocr_val_dict[var_val] = this_org_val_list

    y = None
    while True:
        in_str = yield y

        if len(in_str) == 0:  # Empty string, no modification possible
            y = in_str
            continue

        max_try = 10  # Maximum number of tries to find an OCR modification at a
        # randomly selected position

        done_ocr_mod = False  # A flag, set to True once a modification is done
        try_num = 0

        mod_str = in_str[:]  # Make a copy of the string which will be modified

        while (done_ocr_mod == False) and (try_num < max_try):

            mod_pos = position_function(mod_str)

            # Try one to three characters at selected position
            #
            ocr_org_char_set = {mod_str[mod_pos], mod_str[mod_pos:mod_pos + 2], mod_str[mod_pos:mod_pos + 3]}

            mod_options = []  # List of possible modifications that can be applied

            for ocr_org_char in ocr_org_char_set:
                if ocr_org_char in ocr_val_dict:
                    ocr_var_list = ocr_val_dict[ocr_org_char]
                    for mod_val in ocr_var_list:
                        mod_options.append([ocr_org_char, len(ocr_org_char), mod_val])

            if mod_options != []:  # Modifications are possible

                # Randomly select one of the possible modifications that can be applied
                #
                mod_to_apply = random.choice(mod_options)
                assert mod_to_apply[0] in ocr_val_dict.keys()
                assert mod_to_apply[2] in ocr_val_dict.keys()

                mod_str = in_str[:mod_pos] + mod_to_apply[2] + in_str[mod_pos + mod_to_apply[1]:]

                done_ocr_mod = True

            else:
                try_num += 1

        y = mod_str

def keyboard_corruptor(row_prob,col_prob ) -> Generator[None]:
    position_function = position_mod_normal

    if (abs((row_prob + col_prob) - 1.0) > 0.0000001):
        raise Exception('Sum of row and column probablities does not sum to 1.0')

    #
    rows = {'a': 's',  'b': 'vn', 'c': 'xv', 'd': 'sf', 'e': 'wr', 'f': 'dg',
            'g': 'fh', 'h': 'gj', 'i': 'uo', 'j': 'hk', 'k': 'jl', 'l': 'k',
            'm': 'n',  'n': 'bm', 'o': 'ip', 'p': 'o',  'q': 'w',  'r': 'et',
            's': 'ad', 't': 'ry', 'u': 'yi', 'v': 'cb', 'w': 'qe', 'x': 'zc',
            'y': 'tu', 'z': 'x',
            '1': '2',  '2': '13', '3': '24', '4': '35', '5': '46', '6': '57',
            '7': '68', '8': '79', '9': '80', '0': '9'}

    cols = {'a': 'qzw', 'b': 'gh',  'c': 'df', 'd': 'erc', 'e': 'ds34',
            'f': 'rvc', 'g': 'tbv', 'h': 'ybn', 'i': 'k89',  'j': 'umn',
            'k': 'im', 'l': 'o', 'm': 'jk',  'n': 'hj',  'o': 'l90', 'p': '0',
            'q': 'a12', 'r': 'f45', 's': 'wxz', 't': 'g56',  'u': 'j78',
            'v': 'fg', 'w': 's23',  'x': 'sd', 'y': 'h67',  'z': 'as',
            '1': 'q',  '2': 'qw', '3': 'we', '4': 'er', '5': 'rt',  '6': 'ty',
            '7': 'yu', '8': 'ui', '9': 'io', '0': 'op'}

    y = None
    while True:
        in_str = yield y
        if (len(in_str) == 0):  # Empty string, no modification possible
            y =  in_str
            continue

        max_try = 10  # Maximum number of tries to find a keyboard modification at
        # a randomly selected position

        done_key_mod = False  # A flag, set to true once a modification is done
        try_num = 0

        mod_str = in_str[:]  # Make a copy of the string which will be modified

        while ((done_key_mod == False) and (try_num < max_try)):

            mod_pos = position_function(mod_str)
            mod_char = mod_str[mod_pos]

            r = random.random()  # Create a random number between 0 and 1

            if (r <= row_prob):  # See if there is a row modification
                if (mod_char in rows):
                    key_mod_chars = rows[mod_char]
                    done_key_mod = True

            else:  # See if there is a column modification
                if (mod_char in cols):
                    key_mod_chars = cols[mod_char]
                    done_key_mod = True

            if (done_key_mod == False):
                try_num += 1

        if (done_key_mod == True):
            new_char = random.choice(key_mod_chars)
            mod_str = mod_str[:mod_pos] + new_char + mod_str[mod_pos+1:]

        assert len(mod_str) == len(in_str)
        y = mod_str
