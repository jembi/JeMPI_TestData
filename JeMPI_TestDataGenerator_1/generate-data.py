# generate-data.py - Python module to generate synthetic data based on
#                    look-up files and error tables for Record Linkage purpose.
#
# The original program with some attributes was written by Peter Christen
# and Dinusha Vatsalan in January-March 2012.
# Modified by Sepideh Mosaferi 07/01/2017.
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

import json
import random
import sys

import attrgenfunct  # Functions to generate independent attribute values
# Import the necessary other modules of the data generator
#
import basefunctions  # Helper functions
import corruptor  # Main classes to corrupt attribute values and records
import generator  # Main classes to generate records and the data set

random.seed(42)  # Set seed for random generator, so data generation can
#                       be repeated

#      a  = no corruption
#      b  = only missing values
#      c  = only corrupted values
#      d  = missing & corrupted values#
#     01  = no fields corrupted
#     14  = only gender, date of birth, city corruptible
#     19  = only given name, family name, phone number, national id corruptible
#     20  = all fields corruptible



#f = open('config-test-32-d-001000-004000.json')
if len(sys.argv) != 2:
  sys.exit()

f = open(str(sys.argv[1]))
config1 = json.load(f)
config2 = json.load(open(config1['config2']))

# define variables (this section is in separate cells in the notebook)
# @title Data Generator Variables

# NB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# NB - do not change the index order !!!
# NB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ATTR_NAME = config2['attribute'][0]['name']
ATTR_LAST_NAME = config2['attribute'][1]['name']
ATTR_GENDER = config2['attribute'][2]['name']
ATTR_DOB = config2['attribute'][3]['name']
ATTR_CITY = config2['attribute'][4]['name']
ATTR_PHONE_NUMBER = config2['attribute'][5]['name']
ATTR_NATIONAL_ID = config2['attribute'][6]['name']
ATTR_DUMMY1 = config2['attribute'][7]['name']
ATTR_DUMMY2 = config2['attribute'][8]['name']
ATTR_DUMMY3 = config2['attribute'][9]['name']

# Set the Unicode encoding for this data generation project. This needs to be
# changed to another encoding for different Unicode character sets.
# Valid encoding strings are listed here:
# http://docs.python.org/library/codecs.html#standard-encodings
#
unicode_encoding_used = 'utf_8'

# The name of the record identifier attribute (unique value for each record).
# This name cannot be given as name to any other attribute that is generated.
#
rec_id_attr_name = 'ID'

# Set how many original and how many duplicate records are to be generated.
#
num_org_rec = int(config1['num_org_rec'])
num_dup_rec = int(config1['num_dup_rec'])

# Set the file name of the data set to be generated (this will be a comma
# separated values, CSV, file).
#
# out_file_name = 'data-{}-{}.csv'.format(num_org_rec, num_dup_rec)
out_file_name = 'test-data/' + config1['file_name']

# Set the file name of the data set to be generated (this will be
# Set the maximum number of duplicate records can be generated per original
# record.
#
max_duplicate_per_record = config1['max_duplicate_per_record']

# Set the probability distribution used to create the duplicate records for one
# original record (possible values are: 'uniform', 'poisson', 'zipf').
#
num_duplicates_distribution = config2['num_duplicates_distribution']

# Set the maximum number of modification that can be applied to a single
# attribute (field).
#
max_modification_per_attr = config2['max_modification_per_attr']

# Set the number of modification that are to be applied to a record.
#
num_modification_per_record = config2['num_modification_per_record']

# Check if the given the unicode encoding selected is valid.
#
basefunctions.check_unicode_encoding_exists(unicode_encoding_used)

# -----------------------------------------------------------------------------
# Define the attributes to be generated (using methods from the generator.py
# module).
#

name_gender_attr = \
    generator.GenerateCateCateCompoundAttribute(
        categorical1_attribute_name=ATTR_NAME,
        categorical2_attribute_name=ATTR_GENDER,
        lookup_file_name='lookup-files/given-name-gender-freq.csv',
        has_header_line=False,
        unicode_encoding=unicode_encoding_used)

lastName_attr = \
    generator.GenerateFreqAttribute(
        attribute_name=ATTR_LAST_NAME,
        freq_file_name='lookup-files/family-name-freq.csv',
        has_header_line=False,
        unicode_encoding=unicode_encoding_used)


date_of_birth_attr = \
    generator.GenerateFuncAttribute(
        attribute_name=ATTR_DOB,
        function=attrgenfunct.generate_date_of_birth,
        parameters=[20, 30])

city_attr = \
    generator.GenerateFreqAttribute(
        attribute_name=ATTR_CITY,
        freq_file_name='lookup-files/city-freq.csv',
        has_header_line=False,
        unicode_encoding=unicode_encoding_used)

phone_num_attr = \
    generator.GenerateFuncAttribute(
        attribute_name=ATTR_PHONE_NUMBER,
        function=attrgenfunct.generate_phone_number_ethiopia)

national_id_attr = \
    generator.GenerateFuncAttribute(
        attribute_name=ATTR_NATIONAL_ID,
        function=attrgenfunct.generate_national_id_number)

dummy1_attr = \
    generator.GenerateFuncAttribute(
        attribute_name=ATTR_DUMMY1,
        function=attrgenfunct.generate_date_of_birth,
        parameters=[0, 100])

dummy2_attr = \
    generator.GenerateFuncAttribute(
        attribute_name=ATTR_DUMMY2,
        function=attrgenfunct.generate_date_of_birth,
        parameters=[0, 100])

dummy3_attr = \
    generator.GenerateFuncAttribute(
        attribute_name=ATTR_DUMMY3,
        function=attrgenfunct.generate_date_of_birth,
        parameters=[0, 100])

# -----------------------------------------------------------------------------
# Define how the generated records are to be corrupted (using methods from
# the corruptor.py module).

# For a value edit corruptor, the sum or the four probabilities given must
# be 1.0.
#
edit1_corruptor = \
    corruptor.CorruptValueEdit(
        position_function=getattr(corruptor, config2['corruptor']['edit1']['position_function']),
        char_set_funct=getattr(basefunctions, config2['corruptor']['edit1']['char_set_funct']),
        insert_prob=config2['corruptor']['edit1']['insert_prob'],
        delete_prob=config2['corruptor']['edit1']['delete_prob'],
        substitute_prob=config2['corruptor']['edit1']['substitute_prob'],
        transpose_prob=config2['corruptor']['edit1']['transpose_prob'])

edit2_corruptor = \
    corruptor.CorruptValueEdit(
        position_function=getattr(corruptor, config2['corruptor']['edit2']['position_function']),
        char_set_funct=getattr(basefunctions, config2['corruptor']['edit2']['char_set_funct']),
        insert_prob=config2['corruptor']['edit2']['insert_prob'],
        delete_prob=config2['corruptor']['edit2']['delete_prob'],
        substitute_prob=config2['corruptor']['edit2']['substitute_prob'],
        transpose_prob=config2['corruptor']['edit2']['transpose_prob'])

given_name_misspell_corruptor = \
    corruptor.CorruptCategoricalValue(
        lookup_file_name=config2['corruptor']['given_name_misspell']['lookup_file_name'],
        has_header_line=False,
        unicode_encoding=unicode_encoding_used)

family_name_misspell_corruptor = \
    corruptor.CorruptCategoricalValue(
        lookup_file_name=config2['corruptor']['family_name_misspell']['lookup_file_name'],
        has_header_line=False,
        unicode_encoding=unicode_encoding_used)

ocr_corruptor = corruptor.CorruptValueOCR(
    position_function=corruptor.position_mod_normal,
    lookup_file_name='lookup-files/ocr-variations.csv',
    has_header_line=False,
    unicode_encoding=unicode_encoding_used)

keyboard_corruptor = corruptor.CorruptValueKeyboard(
    position_function=corruptor.position_mod_normal,
    row_prob=0.5,
    col_prob=0.5)

phonetic_corruptor = corruptor.CorruptValuePhonetic(
    lookup_file_name='lookup-files/phonetic-variations.csv',
    has_header_line=False,
    unicode_encoding=unicode_encoding_used)

missing_val_corruptor = corruptor.CorruptMissingValue()

# -----------------------------------------------------------------------------
# Define the attributes to be generated for this data set, and the data set
# itself.
#
attr_name_list = [config2['attribute'][0]['name'],
                  config2['attribute'][1]['name'],
                  config2['attribute'][2]['name'],
                  config2['attribute'][3]['name'],
                  config2['attribute'][4]['name'],
                  config2['attribute'][5]['name'],
                  config2['attribute'][6]['name'],
                  config2['attribute'][7]['name'],
                  config2['attribute'][8]['name'],
                  config2['attribute'][9]['name']]

attr_data_list = [name_gender_attr,
                  lastName_attr,
                  date_of_birth_attr,
                  city_attr,
                  phone_num_attr,
                  national_id_attr,
                  dummy1_attr,
                  dummy2_attr,
                  dummy3_attr]

# Nothing to change here - set-up the data set generation object.
#
test_data_generator = generator.GenerateDataSet(
    output_file_name=out_file_name,
    write_header_line=True,
    rec_id_attr_name=rec_id_attr_name,
    number_of_records=num_org_rec,
    attribute_name_list=attr_name_list,
    attribute_data_list=attr_data_list,
    unicode_encoding=unicode_encoding_used)

# Define the probability distribution of how likely an attribute will be
# selected for a modification.
# Each of the given probability values must be between 0 and 1, and the sum of
# them must be 1.0.
# If a probability is set to 0 for a certain attribute, then no modification
# will be applied on this attribute.
#
attr_mod_prob_dictionary = {
    config2['attribute'][0]['name']: config2['attribute'][0]['corruption_prob'],
    config2['attribute'][1]['name']: config2['attribute'][1]['corruption_prob'],
    config2['attribute'][2]['name']: config2['attribute'][2]['corruption_prob'],
    config2['attribute'][3]['name']: config2['attribute'][3]['corruption_prob'],
    config2['attribute'][4]['name']: config2['attribute'][4]['corruption_prob'],
    config2['attribute'][5]['name']: config2['attribute'][5]['corruption_prob'],
    config2['attribute'][6]['name']: config2['attribute'][6]['corruption_prob'],
    config2['attribute'][7]['name']: config2['attribute'][7]['corruption_prob'],
    config2['attribute'][8]['name']: config2['attribute'][8]['corruption_prob'],
    config2['attribute'][9]['name']: config2['attribute'][9]['corruption_prob']
}

# Define the actual corruption (modification) methods that will be applied on
# the different attributes.
# For each attribute, the sum of probabilities given must sum to 1.0.
#
attr_mod_data_dictionary = {
    config2['attribute'][0]['name']: [  # GIVEN NAME
        (config2['attribute'][0]['corruptor_prob']['missing_val'], missing_val_corruptor),
        (config2['attribute'][0]['corruptor_prob']['name_misspell'], given_name_misspell_corruptor),
        (config2['attribute'][0]['corruptor_prob']['edit1'], edit1_corruptor),
        (config2['attribute'][0]['corruptor_prob']['edit2'], edit2_corruptor),
        (config2['attribute'][0]['corruptor_prob']['ocr'], ocr_corruptor),
        (config2['attribute'][0]['corruptor_prob']['keyboard'], keyboard_corruptor),
        (config2['attribute'][0]['corruptor_prob']['phonetic'], phonetic_corruptor)],
    config2['attribute'][1]['name']: [  # FAMILY NAME
        (config2['attribute'][1]['corruptor_prob']['missing_val'], missing_val_corruptor),
        (config2['attribute'][1]['corruptor_prob']['name_misspell'], family_name_misspell_corruptor),
        (config2['attribute'][1]['corruptor_prob']['edit1'], edit1_corruptor),
        (config2['attribute'][1]['corruptor_prob']['edit2'], edit2_corruptor),
        (config2['attribute'][1]['corruptor_prob']['ocr'], ocr_corruptor),
        (config2['attribute'][1]['corruptor_prob']['keyboard'], keyboard_corruptor),
        (config2['attribute'][1]['corruptor_prob']['phonetic'], phonetic_corruptor)],
    config2['attribute'][2]['name']: [  # GENDER
        (config2['attribute'][2]['corruptor_prob']['missing_val'], missing_val_corruptor),
        (config2['attribute'][2]['corruptor_prob']['name_misspell'], None),
        (config2['attribute'][2]['corruptor_prob']['edit1'], edit1_corruptor),
        (config2['attribute'][2]['corruptor_prob']['edit2'], edit2_corruptor),
        (config2['attribute'][2]['corruptor_prob']['ocr'], ocr_corruptor),
        (config2['attribute'][2]['corruptor_prob']['keyboard'], keyboard_corruptor),
        (config2['attribute'][2]['corruptor_prob']['phonetic'], phonetic_corruptor)],
    config2['attribute'][3]['name']: [  # DATE OF BIRTH
        (config2['attribute'][3]['corruptor_prob']['missing_val'], missing_val_corruptor),
        (config2['attribute'][3]['corruptor_prob']['name_misspell'], None),
        (config2['attribute'][3]['corruptor_prob']['edit1'], edit1_corruptor),
        (config2['attribute'][3]['corruptor_prob']['edit2'], edit2_corruptor),
        (config2['attribute'][3]['corruptor_prob']['ocr'], ocr_corruptor),
        (config2['attribute'][3]['corruptor_prob']['keyboard'], keyboard_corruptor),
        (config2['attribute'][3]['corruptor_prob']['phonetic'], phonetic_corruptor)],
    config2['attribute'][4]['name']: [  # CITY
        (config2['attribute'][4]['corruptor_prob']['missing_val'], missing_val_corruptor),
        (config2['attribute'][4]['corruptor_prob']['name_misspell'], None),
        (config2['attribute'][4]['corruptor_prob']['edit1'], edit1_corruptor),
        (config2['attribute'][4]['corruptor_prob']['edit2'], edit2_corruptor),
        (config2['attribute'][4]['corruptor_prob']['ocr'], ocr_corruptor),
        (config2['attribute'][4]['corruptor_prob']['keyboard'], keyboard_corruptor),
        (config2['attribute'][4]['corruptor_prob']['phonetic'], phonetic_corruptor)],
    config2['attribute'][5]['name']: [  # PHONE NUMBER
        (config2['attribute'][5]['corruptor_prob']['missing_val'], missing_val_corruptor),
        (config2['attribute'][5]['corruptor_prob']['name_misspell'], None),
        (config2['attribute'][5]['corruptor_prob']['edit1'], edit1_corruptor),
        (config2['attribute'][5]['corruptor_prob']['edit2'], edit2_corruptor),
        (config2['attribute'][5]['corruptor_prob']['ocr'], ocr_corruptor),
        (config2['attribute'][5]['corruptor_prob']['keyboard'], keyboard_corruptor),
        (config2['attribute'][5]['corruptor_prob']['phonetic'], phonetic_corruptor)],
    config2['attribute'][6]['name']: [  # NATIONAL ID
        (config2['attribute'][6]['corruptor_prob']['missing_val'], missing_val_corruptor),
        (config2['attribute'][6]['corruptor_prob']['name_misspell'], None),
        (config2['attribute'][6]['corruptor_prob']['edit1'], edit1_corruptor),
        (config2['attribute'][6]['corruptor_prob']['edit2'], edit2_corruptor),
        (config2['attribute'][6]['corruptor_prob']['ocr'], ocr_corruptor),
        (config2['attribute'][6]['corruptor_prob']['keyboard'], keyboard_corruptor),
        (config2['attribute'][6]['corruptor_prob']['phonetic'], phonetic_corruptor)],
    config2['attribute'][7]['name']: [  # DUMMY
        (config2['attribute'][7]['corruptor_prob']['missing_val'], missing_val_corruptor),
        (config2['attribute'][7]['corruptor_prob']['name_misspell'], None),
        (config2['attribute'][7]['corruptor_prob']['edit1'], edit1_corruptor),
        (config2['attribute'][7]['corruptor_prob']['edit2'], edit2_corruptor),
        (config2['attribute'][7]['corruptor_prob']['ocr'], ocr_corruptor),
        (config2['attribute'][7]['corruptor_prob']['keyboard'], keyboard_corruptor),
        (config2['attribute'][7]['corruptor_prob']['phonetic'], phonetic_corruptor)],
    config2['attribute'][8]['name']: [  # DUMMY
        (config2['attribute'][8]['corruptor_prob']['missing_val'], missing_val_corruptor),
        (config2['attribute'][8]['corruptor_prob']['name_misspell'], None),
        (config2['attribute'][8]['corruptor_prob']['edit1'], edit1_corruptor),
        (config2['attribute'][8]['corruptor_prob']['edit2'], edit2_corruptor),
        (config2['attribute'][8]['corruptor_prob']['ocr'], ocr_corruptor),
        (config2['attribute'][8]['corruptor_prob']['keyboard'], keyboard_corruptor),
        (config2['attribute'][8]['corruptor_prob']['phonetic'], phonetic_corruptor)],
    config2['attribute'][9]['name']: [  # DUMMY
        (config2['attribute'][9]['corruptor_prob']['missing_val'], missing_val_corruptor),
        (config2['attribute'][9]['corruptor_prob']['name_misspell'], None),
        (config2['attribute'][9]['corruptor_prob']['edit1'], edit1_corruptor),
        (config2['attribute'][9]['corruptor_prob']['edit2'], edit2_corruptor),
        (config2['attribute'][9]['corruptor_prob']['ocr'], ocr_corruptor),
        (config2['attribute'][9]['corruptor_prob']['keyboard'], keyboard_corruptor),
        (config2['attribute'][9]['corruptor_prob']['phonetic'], phonetic_corruptor)]
}

# Nothing to change here - set-up the data set corruption object
#
test_data_corruptor = corruptor.CorruptDataSet(
    number_of_org_records=num_org_rec,
    number_of_mod_records=num_dup_rec,
    attribute_name_list=attr_name_list,
    max_num_dup_per_rec=max_duplicate_per_record,
    num_dup_dist=num_duplicates_distribution,
    max_num_mod_per_attr=max_modification_per_attr,
    num_mod_per_rec=num_modification_per_record,
    attr_mod_prob_dict=attr_mod_prob_dictionary,
    attr_mod_data_dict=attr_mod_data_dictionary)

# =============================================================================
# No need to change anything below here

# Start the data generation process
#
rec_dict = test_data_generator.generate()

# Check the number of generated records
assert len(rec_dict) == num_org_rec

# Corrupt (modify) the original records into duplicate records
#
rec_dict = test_data_corruptor.corrupt_records(rec_dict)

# Check total number of records
assert len(rec_dict) == num_org_rec + num_dup_rec

# Write generate data into a file
#
test_data_generator.write()

print()
print(config1['file_name'])
print('num_org_rec:              {0:>8}'.format(config1['num_org_rec']))
print('num_dup_rec:              {0:>8}'.format(config1['num_dup_rec']))
print('num_duplicate_per_record: {0:>8}'.format(config1['max_duplicate_per_record']))
print('{0:<17} {1:>10} {2:>10} {3:>10} {4:>10} {5:>10} {6:>10} {7:>10} {8:>10}'
      .format('attribute', 'prob', 'missing', 'misspell', 'edit1', 'edit2', 'ocr',
              'keyboard', 'phonetic'))
for i in range(10):
    print('{0:<17} {1:10} {2: 10} {3: 10} {4:10} {5:10} {6:10} {7:10} {8:10}'
          .format(config2['attribute'][i]['name'],
                  config2['attribute'][i]['corruption_prob'],
                  config2['attribute'][i]['corruptor_prob']['missing_val'],
                  config2['attribute'][i]['corruptor_prob']['name_misspell'],
                  config2['attribute'][i]['corruptor_prob']['edit1'],
                  config2['attribute'][i]['corruptor_prob']['edit2'],
                  config2['attribute'][i]['corruptor_prob']['ocr'],
                  config2['attribute'][i]['corruptor_prob']['keyboard'],
                  config2['attribute'][i]['corruptor_prob']['phonetic']))

# End.
# =============================================================================
