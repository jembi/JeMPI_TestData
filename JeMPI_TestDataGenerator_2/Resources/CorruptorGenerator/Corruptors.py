import codecs
import random
from collections.abc import Generator

def __apply_change__(in_str, ch):
    """Helper function which will apply the selected change to the input
       string.

       Developed by Agus Pudjijono, ANU, 2008.
    """

    work_str = in_str
    list_ch = ch.split('>')
    subs = list_ch[1]
    if (list_ch[1] == '@'):  # @ is blank
        subs = ''
    tmp_str = work_str
    org_pat_length = len(list_ch[0])
    str_length = len(work_str)

    if (list_ch[2] == 'end'):
        org_pat_start = work_str.find(
            list_ch[0], str_length-org_pat_length)
    elif (list_ch[2] == 'middle'):
        org_pat_start = work_str.find(list_ch[0], 1)
    else:  # Start and all
        org_pat_start = work_str.find(list_ch[0], 0)

    if (org_pat_start == 0):
        work_str = subs + work_str[org_pat_length:]
    elif (org_pat_start > 0):
        work_str = work_str[:org_pat_start] + subs + work_str[org_pat_start+org_pat_length:]

    if (work_str == tmp_str):
        work_str = str_to_change

    return work_str


def position_mod_normal(in_str):
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


def phonetic_corruptor() -> Generator[None]:

    lookup_file_name = 'metadata/phonetic-variations.csv'
    has_header_line = None
    unicode_encoding = 'utf_8'
    replace_table = []

    def dummy_position(s):  # Define a dummy position function
        return 0

    # Process all keyword arguments
    #
    #base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    # for (keyword, value) in kwargs.items():
    #
    #     if (keyword.startswith('look')):
    #         #basefunctions.check_is_non_empty_string('lookup_file_name', value)
    #         lookup_file_name = value
    #
    #     elif (keyword.startswith('has')):
    #         #basefunctions.check_is_flag('has_header_line', value)
    #         has_header_line = value
    #
    #     elif (keyword.startswith('unicode')):
    #         #basefunctions.check_is_non_empty_string('unicode_encoding', value)
    #         unicode_encoding = value
    #
    #     else:
    #         base_kwargs[keyword] = value

    #base_kwargs['position_function'] = dummy_position

    #CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    #basefunctions.check_is_non_empty_string('lookup_file_name',
    #                                        self.lookup_file_name)
    #basefunctions.check_is_flag('has_header_line', self.has_header_line)
    #basefunctions.check_is_non_empty_string('unicode_encoding',
    #                                        self.unicode_encoding)

    # Load the misspelling lookup file - - - - - - - - - - - - - - - - - - - - -
    #
    header_list, lookup_file_data =   read_csv_file(lookup_file_name, unicode_encoding, has_header_line)

    # Process values from file and misspellings
    #
    for rec_list in lookup_file_data:
        if (len(rec_list) != 7):
            raise Exception('Illegal format in phonetic lookup file %s: %s'
                            % (lookup_file_name, str(rec_list)))
        val_tuple = ()
        for val in rec_list:
            if (val != ''):
                val = val.strip()
                val_tuple += val,
            else:
                raise Exception('Empty value in phonetic lookup file %s" %s' %
                                (lookup_file_name, str(rec_list)))
        replace_table.append(val_tuple)

# ---------------------------------------------------------------------------
    y = None
    while True:
        in_str = yield y
        if (len(in_str) == 0):  # Empty string, no modification possible
            y =  in_str
            continue

        work_str = in_str
        list_ch = split('>')
        subs = list_ch[1]
        if (list_ch[1] == '@'):  # @ is blank
            subs = ''
        tmp_str = work_str
        org_pat_length = len(list_ch[0])
        str_length = len(work_str)

        if (list_ch[2] == 'end'):
            org_pat_start = work_str.find(
                list_ch[0], str_length-org_pat_length)
        elif (list_ch[2] == 'middle'):
            org_pat_start = work_str.find(list_ch[0], 1)
        else:  # Start and all
            org_pat_start = work_str.find(list_ch[0], 0)

        if (org_pat_start == 0):
            work_str = subs + work_str[org_pat_length:]
        elif (org_pat_start > 0):
            work_str = work_str[:org_pat_start] + subs + \
                       work_str[org_pat_start+org_pat_length:]

        if (work_str == tmp_str):
            work_str = str_to_change

        return work_str

# ---------------------------------------------------------------------------

def __slavo_germanic__(self, in_str):
    """Helper function which determines if the inputstring could contain a
       Slavo or Germanic name.

       Developed by Agus Pudjijono, ANU, 2008.
    """

    if ((in_str.find('w') > -1) or (in_str.find('k') > -1) or
            (in_str.find('cz') > -1) or (in_str.find('witz') > -1)):
        return 1
    else:
        return 0

# ---------------------------------------------------------------------------

def __collect_replacement__(self, s, where, orgpat, newpat, precond,
                            postcond, existcond, startcond):
    """Helper function which collects all the possible phonetic modification
       patterns that are possible on the given input string, and replaces a
       pattern in a string.

       The following arguments are needed:
       - where     Can be one of: 'ALL','START','END','MIDDLE'
       - precond   Pre-condition (default 'None') can be 'V' for vowel or
                   'C' for consonant
       - postcond  Post-condition (default 'None') can be 'V' for vowel or
                   'C' for consonant

       Developed by Agus Pudjijono, ANU, 2008.
    """

    vowels = 'aeiouy'
    tmpstr = s
    changesstr = ''

    start_search = 0  # Position from where to start the search
    pat_len = len(orgpat)
    stop = False

    # As long as pattern is in string
    #
    while ((orgpat in tmpstr[start_search:]) and (stop == False)):

        pat_start = tmpstr.find(orgpat, start_search)
        str_len = len(tmpstr)

        # Check conditions of previous and following character
        #
        OKpre = False   # Previous character condition
        OKpre1 = False   # Previous character1 condition
        OKpre2 = False   # Previous character2 condition

        OKpost = False  # Following character condition
        OKpost1 = False  # Following character1 condition
        OKpost2 = False  # Following character2 condition

        OKexist = False  # Existing pattern condition
        OKstart = False  # Existing start pattern condition

        index = 0

        if (precond == 'None'):
            OKpre = True

        elif (pat_start > 0):
            if (((precond == 'V') and (tmpstr[pat_start-1] in vowels)) or
                    ((precond == 'C') and (tmpstr[pat_start-1] not in vowels))):
                OKpre = True

            elif ((precond.find(';')) > -1):
                if (precond.find('|') > -1):
                    rls = precond.split('|')
                    rl1 = rls[0].split(';')

                    if (int(rl1[1]) < 0):
                        index = pat_start+int(rl1[1])
                    else:
                        index = pat_start+(len(orgpat)-1)+int(rl1[1])

                    i = 2
                    if (rl1[0] == 'n'):
                        while (i < (len(rl1))):
                            if (tmpstr[index:(index+len(rl1[i]))] == rl1[i]):
                                OKpre1 = False
                                break
                            else:
                                OKpre1 = True
                            i += 1
                    else:
                        while (i < (len(rl1))):
                            if (tmpstr[index:(index+len(rl1[i]))] == rl1[i]):
                                OKpre1 = True
                                break
                            i += 1

                    rl2 = rls[1].split(';')

                    if (int(rl2[1]) < 0):
                        index = pat_start+int(rl2[1])
                    else:
                        index = pat_start+(len(orgpat)-1)+int(rl2[1])

                    i = 2
                    if (rl2[0] == 'n'):
                        while (i < (len(rl2))):
                            if (tmpstr[index:(index+len(rl2[i]))] == rl2[i]):
                                OKpre2 = False
                                break
                            else:
                                OKpre2 = True
                            i += 1
                    else:
                        while (i < (len(rl2))):
                            if (tmpstr[index:(index+len(rl2[i]))] == rl2[i]):
                                OKpre2 = True
                                break
                            i += 1

                    OKpre = OKpre1 and OKpre2

                else:
                    rl = precond.split(';')
                    # -
                    if (int(rl[1]) < 0):
                        index = pat_start+int(rl[1])
                    else:
                        index = pat_start+(len(orgpat)-1)+int(rl[1])

                    i = 2
                    if (rl[0] == 'n'):
                        while (i < (len(rl))):
                            if (tmpstr[index:(index+len(rl[i]))] == rl[i]):
                                OKpre = False
                                break
                            else:
                                OKpre = True
                            i += 1
                    else:
                        while (i < (len(rl))):
                            if (tmpstr[index:(index+len(rl[i]))] == rl[i]):
                                OKpre = True
                                break
                            i += 1

        if (postcond == 'None'):
            OKpost = True

        else:
            pat_end = pat_start+pat_len

            if (pat_end < str_len):
                if (((postcond == 'V') and (tmpstr[pat_end] in vowels)) or
                        ((postcond == 'C') and (tmpstr[pat_end] not in vowels))):
                    OKpost = True
                elif ((postcond.find(';')) > -1):
                    if (postcond.find('|') > -1):
                        rls = postcond.split('|')

                        rl1 = rls[0].split(';')

                        if (int(rl1[1]) < 0):
                            index = pat_start+int(rl1[1])
                        else:
                            index = pat_start+(len(orgpat)-1)+int(rl1[1])

                        i = 2
                        if (rl1[0] == 'n'):
                            while (i < (len(rl1))):
                                if (tmpstr[index:(index+len(rl1[i]))] == rl1[i]):
                                    OKpost1 = False
                                    break
                                else:
                                    OKpost1 = True
                                i += 1
                        else:
                            while (i < (len(rl1))):
                                if (tmpstr[index:(index+len(rl1[i]))] == rl1[i]):
                                    OKpost1 = True
                                    break
                                i += 1

                        rl2 = rls[1].split(';')

                        if (int(rl2[1]) < 0):
                            index = pat_start+int(rl2[1])
                        else:
                            index = pat_start+(len(orgpat)-1)+int(rl2[1])

                        i = 2
                        if (rl2[0] == 'n'):
                            while (i < (len(rl2))):
                                if (tmpstr[index:(index+len(rl2[i]))] == rl2[i]):
                                    OKpost2 = False
                                    break
                                else:
                                    OKpost2 = True
                                i += 1
                        else:
                            while (i < (len(rl2))):
                                if (tmpstr[index:(index+len(rl2[i]))] == rl2[i]):
                                    OKpost2 = True
                                    break
                                i += 1

                        OKpost = OKpost1 and OKpost2

                    else:
                        rl = postcond.split(';')

                        if (int(rl[1]) < 0):
                            index = pat_start+int(rl[1])
                        else:
                            index = pat_start+(len(orgpat)-1)+int(rl[1])

                        i = 2
                        if (rl[0] == 'n'):
                            while (i < (len(rl))):
                                if (tmpstr[index:(index+len(rl[i]))] == rl[i]):
                                    OKpost = False
                                    break
                                else:
                                    OKpost = True
                                i += 1
                        else:
                            while (i < (len(rl))):
                                if (tmpstr[index:(index+len(rl[i]))] == rl[i]):
                                    OKpost = True
                                    break
                                i += 1

        if (existcond == 'None'):
            OKexist = True

        else:
            rl = existcond.split(';')
            if (rl[1] == 'slavo'):
                r = self.__slavo_germanic__(s)
                if (rl[0] == 'n'):
                    if (r == 0):
                        OKexist = True
                else:
                    if (r == 1):
                        OKexist = True
            else:
                i = 1
                if (rl[0] == 'n'):
                    while (i < (len(rl))):
                        if (s.find(rl[i]) > -1):
                            OKexist = False
                            break
                        else:
                            OKexist = True
                        i += i
                else:
                    while (i < (len(rl))):
                        if (s.find(rl[i]) > -1):
                            OKexist = True
                            break
                        i += i

        if (startcond == 'None'):
            OKstart = True

        else:
            rl = startcond.split(';')
            i = 1
            if (rl[0] == 'n'):
                while (i < (len(rl))):
                    if (s.find(rl[i]) > -1):
                        OKstart = False
                        break
                    else:
                        OKstart = True
                    i += i
            else:
                while (i < (len(rl))):
                    if (s.find(rl[i]) == 0):
                        OKstart = True
                        break
                    i += i

        # Replace pattern if conditions and position OK
        #
        if ((OKpre == True) and (OKpost == True) and (OKexist == True) and
            (OKstart == True)) and (((where == 'START') and (pat_start == 0))
                                    or ((where == 'MIDDLE') and (pat_start > 0) and
                                        (pat_start+pat_len < str_len)) or ((where == 'END') and
                                                                           (pat_start+pat_len == str_len)) or (where == 'ALL')):
            tmpstr = tmpstr[:pat_start]+newpat+tmpstr[pat_start+pat_len:]
            changesstr += ',' + orgpat + '>' + newpat + '>' + where.lower()
            start_search = pat_start + len(newpat)

        else:
            start_search = pat_start+1

        if (start_search >= (len(tmpstr)-1)):
            stop = True

    tmpstr += changesstr

    return tmpstr

# ---------------------------------------------------------------------------

def __get_transformation__(self, in_str):
    """Helper function which generates the list of possible phonetic
       modifications for the given input string.

       Developed by Agus Pudjijono, ANU, 2008.
    """

    if (in_str == ''):
        return in_str

    changesstr2 = ''

    workstr = in_str

    for rtpl in self.replace_table:  # Check all transformations in the table
        if (len(rtpl) == 3):
            rtpl += ('None', 'None', 'None', 'None')

        workstr = self.__collect_replacement__(in_str, rtpl[0], rtpl[1], rtpl[2],
                                               rtpl[3], rtpl[4], rtpl[5], rtpl[6])
        if (workstr.find(',') > -1):
            tmpstr = workstr.split(',')
            workstr = tmpstr[0]
            if (changesstr2.find(tmpstr[1]) == -1):
                changesstr2 += tmpstr[1]+';'
    workstr += ',' + changesstr2

    return workstr

# ---------------------------------------------------------------------------

def corrupt_value(self, in_str):
    """Method which corrupts the given input string by applying a phonetic
       modification.

       If several such modifications are possible then one will be randomly
       selected.
    """

    if (len(in_str) == 0):  # Empty string, no modification possible
        return in_str

    # Get the possible phonetic modifications for this input string
    #
    phonetic_changes = self.__get_transformation__(in_str)

    mod_str = in_str

    if (',' in phonetic_changes):  # Several modifications possible
        tmp_str = phonetic_changes.split(',')
        pc = tmp_str[1][:-1]  # Remove the last ';'
        list_pc = pc.split(';')
        change_op = random.choice(list_pc)
        if (change_op != ''):
            mod_str = __apply_change__(in_str, change_op)
            # print in_str, mod_str, change_op

    return mod_str
