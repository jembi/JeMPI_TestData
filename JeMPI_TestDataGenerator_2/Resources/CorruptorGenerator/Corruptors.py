import codecs
import random
from collections.abc import Generator


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
