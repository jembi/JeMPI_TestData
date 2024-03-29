import numpy as np
import pandas as pd

from Resources.ClinicalDataGenerator import MinimalClinicalDataGenerator
from Resources.CorrupterGenerator import Corrupters
from Resources.DemographicDataGenerator import PatientGenerator
from Utilities import helper, basefunctions

config_corrupt_nupi = \
    {"BaseDate": "2022-01-01",
     "NumberOfPatients": 1_000,
     "AverageNumberOfClinicalRecordsPerPatient": 5,
     "PercentageOfCorruptedRecords": 0.1,
     "fields": [
         {"name": "phonetic_given_name",
          "weight": 0.0,
          "corrupter": {
              "type": ["missing_value_corrupter", "keyboard_corrupter", "edit1_corrupter", "edit2_corrupter",
                       "phonetic_corrupter", "ocr_corrupter"],
              "weight": [0.0, 0.0, 0.0, 0.0, 1.0, 0.0]}},
         {"name": "phonetic_family_name",
          "weight": 0.0,
          "corrupter": {
              "type": ["missing_value_corrupter", "keyboard_corrupter", "edit1_corrupter", "edit2_corrupter",
                       "phonetic_corrupter", "ocr_corrupter"],
              "weight": [0.0, 0.0, 0.0, 0.0, 1.0, 0.0]}},
         {"name": "gender",
          "weight": 0.0,
          "corrupter": {
              "type": ["missing_value_corrupter", "keyboard_corrupter", "edit1_corrupter", "edit2_corrupter",
                       "phonetic_corrupter", "ocr_corrupter"],
              "weight": [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]}},
         {"name": "dob",
          "weight": 0.0,
          "corrupter": {
              "type": ["missing_value_corrupter", "keyboard_corrupter", "edit1_corrupter", "edit2_corrupter",
                       "phonetic_corrupter", "ocr_corrupter"],
              "weight": [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]}},
         {"name": "nupi",
          "weight": 1.0,
          "corrupter": {
              "type": ["missing_value_corrupter", "keyboard_corrupter", "edit1_corrupter", "edit2_corrupter",
                       "phonetic_corrupter", "ocr_corrupter"],
              "weight": [0.6, 0.0, 0.1, 0.1, 0.0, 0.2]}},
     ]}

config_corrupt_nupi_pkv = \
    {"BaseDate": "2022-01-01",
     "NumberOfPatients": 1_000,
     "AverageNumberOfClinicalRecordsPerPatient": 5,
     "PercentageOfCorruptedRecords": 0.1,
     "fields": [
         {"name": "phonetic_given_name",
          "weight": 0.15,
          "corrupter": {
              "type": ["missing_value_corrupter", "keyboard_corrupter", "edit1_corrupter", "edit2_corrupter",
                       "phonetic_corrupter", "ocr_corrupter"],
              "weight": [0.0, 0.0, 0.0, 0.0, 1.0, 0.0]}},
         {"name": "phonetic_family_name",
          "weight": 0.15,
          "corrupter": {
              "type": ["missing_value_corrupter", "keyboard_corrupter", "edit1_corrupter", "edit2_corrupter",
                       "phonetic_corrupter", "ocr_corrupter"],
              "weight": [0.0, 0.0, 0.0, 0.0, 1.0, 0.0]}},
         {"name": "gender",
          "weight": 0.05,
          "corrupter": {
              "type": ["missing_value_corrupter", "keyboard_corrupter", "edit1_corrupter", "edit2_corrupter",
                       "phonetic_corrupter", "ocr_corrupter"],
              "weight": [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]}},
         {"name": "dob",
          "weight": 0.05,
          "corrupter": {
              "type": ["missing_value_corrupter", "keyboard_corrupter", "edit1_corrupter", "edit2_corrupter",
                       "phonetic_corrupter", "ocr_corrupter"],
              "weight": [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]}},
         {"name": "nupi",
          "weight": 0.6,
          "corrupter": {
              "type": ["missing_value_corrupter", "keyboard_corrupter", "edit1_corrupter", "edit2_corrupter",
                       "phonetic_corrupter", "ocr_corrupter"],
              "weight": [0.6, 0.0, 0.1, 0.1, 0.0, 0.2]}},
     ]}

config = config_corrupt_nupi_pkv

seed = 123456
rng = np.random.default_rng(seed)
base_date = config['BaseDate']
number_of_patients = config.get("NumberOfPatients")
gender_generator = PatientGenerator.gender_generator(seed, 0.50)
phonetic_male_name_generator = PatientGenerator.name_generator(seed, 'metadata/name-m-freq.csv')
phonetic_female_name_generator = PatientGenerator.name_generator(seed, 'metadata/name-f-freq.csv')
phonetic_family_name_generator = PatientGenerator.name_generator(seed, 'metadata/family-name-freq.csv')
dob_generator = PatientGenerator.date_generator(seed, base_date, 'gumbel', 35, 12 * 10)
nupi_generator = PatientGenerator.national_id_generator(seed)
clinical_data_generator = MinimalClinicalDataGenerator.clinical_data_generator(
    seed,
    config['AverageNumberOfClinicalRecordsPerPatient'])
corrupter_dict = {'ocr_corrupter': Corrupters.ocr_corrupter('metadata/ocr-variations.csv', False, None,
                                                            Corrupters.position_mod_normal),
                  'missing_value_corrupter': Corrupters.missing_value_corrupter(),
                  'keyboard_corrupter': Corrupters.keyboard_corrupter(0.5, 0.5, Corrupters.position_mod_normal),
                  'edit1_corrupter': Corrupters.edit_corrupter(Corrupters.position_mod_normal,
                                                               basefunctions.char_set_ascii,
                                                               0.50, 0.50, 0.00, 0.00),
                  'edit2_corrupter': Corrupters.edit_corrupter(Corrupters.position_mod_uniform,
                                                               basefunctions.char_set_ascii,
                                                               0.25, 0.25, 0.25, 0.25),
                  'phonetic_corrupter': Corrupters.phonetic_corrupter('metadata/phonetic-variations.csv',
                                                                      False, 'utf_8')}
next(nupi_generator)
next(clinical_data_generator)
next(corrupter_dict['missing_value_corrupter'])
next(corrupter_dict['ocr_corrupter'])
next(corrupter_dict['keyboard_corrupter'])
next(corrupter_dict['edit1_corrupter'])
next(corrupter_dict['edit2_corrupter'])
next(corrupter_dict['phonetic_corrupter'])

field_name_list = []
field_weight_list = []
field_corrupter_name_set = {}
field_corrupter_weight_set = {}


def generate_patients():
    data = []
    k = 0
    for i in range(0, number_of_patients):
        k = k + 1
        if k % 5000 == 0:
            print(k)
        gender = next(gender_generator)
        phonetic_given_name = next(phonetic_female_name_generator)[1] if gender == 'female' else next(phonetic_male_name_generator)[1]
        phonetic_family_name = next(phonetic_family_name_generator)[1]
        dob = next(dob_generator)
        dob = np.datetime_as_string(dob, unit='D')
        nupi = nupi_generator.send((dob, gender))
        clinical_data = clinical_data_generator.send((gender, base_date, dob, nupi))
        for j in range(0, len(clinical_data)):
            rec_num = "rec-%010d-%02d" % (i + 1, j)
            data.append([rec_num, phonetic_given_name, phonetic_family_name, gender, dob, nupi, clinical_data[j]])
    return data


def corrupt_data(df):
    df['corrupted'] = False
    number_of_records = df.shape[0]
    percentage_of_corrupted_records = config['PercentageOfCorruptedRecords']
    number_of_corrupted_records = int(number_of_records * percentage_of_corrupted_records)
    k = 0
    for _ in range(0, number_of_corrupted_records):
        k = k + 1
        if k % 1000 == 0:
            print(k)
        candidate_not_corrupted = False
        row_to_corrupt = None
        while not candidate_not_corrupted:
            row_to_corrupt = rng.integers(0, number_of_records)
            already_corrupted = df.loc[row_to_corrupt]['corrupted']
            if not already_corrupted:
                df.at[row_to_corrupt, 'corrupted'] = True
                candidate_not_corrupted = True
        columns_to_corrupt = rng.choice(a=field_name_list,
                                        p=field_weight_list,
                                        size=rng.integers(1, len(field_weight_list) + 1),
                                        replace=False)
        # columns_to_corrupt = ['nupi']
        # print('row to corrupt: %s' % row_to_corrupt)
        for column_to_corrupt in columns_to_corrupt:
            corrupter_names = field_corrupter_name_set[column_to_corrupt]
            corrupter_weights = field_corrupter_weight_set[column_to_corrupt]
            corrupter = rng.choice(a=corrupter_names, p=corrupter_weights, size=1, replace=False)[0]
            # print('col to corrupt: %s, %s' % (column_to_corrupt, corrupter))
            value_to_corrupt = df.at[row_to_corrupt, column_to_corrupt]
            corrupter_value = corrupter_dict[corrupter].send(value_to_corrupt)
            df.at[row_to_corrupt, column_to_corrupt] = corrupter_value
        # print()
    return df.drop('corrupted', axis=1)


def generate_dataset():
    fields = config["fields"]
    for f_idx in range(len(fields)):
        field_name_list.append(fields[f_idx]['name'])
        field_weight_list.append(fields[f_idx]['weight'])
        field_corrupter_name_set[fields[f_idx]['name']] = fields[f_idx]['corrupter']['type']
        field_corrupter_weight_set[fields[f_idx]['name']] = fields[f_idx]['corrupter']['weight']
    data = generate_patients()
    df = pd.DataFrame(data,
                      columns=['rec_num', 'phonetic_given_name', 'phonetic_family_name', 'gender', 'dob', 'nupi',
                               'clinical_data'])
    df = corrupt_data(df)
    csv_file_name = 'Results/' + str(helper.generate_log_filename('synthetic_data_kenya_V'))
    df.to_csv(csv_file_name, index=False, encoding='utf-8')


def main():
    generate_dataset()


main()
