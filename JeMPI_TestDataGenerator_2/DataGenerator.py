import random

import numpy as np
import pandas as pd

from Resources.ClinicalDataGenerator import MinimalClinicalDataGenerator
from Resources.CorruptorGenerator import Corruptors
from Resources.DemographicDataGenerator import PatientGenerator
from Utilities import helper, basefunctions


def generate_dataset():
    config = \
        {"BaseDate": "2022-01-01",
         "NumberOfPatients": 100_000,
         "AverageNumberOfClinicalRecordsPerPatient": 10,
         "PercentageOfCorruptedRecords": 0.8,
         "fields": [
             {"name": "given_name",
              "weight": 0.2,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.2, 0.2, 0.2, 0.1, 0.15, 0.15]}},
             {"name": "fathers_name",
              "weight": 0.2,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.2, 0.3, 0.1, 0.1, 0.1, 0.2]}},
             {"name": "fathers_father_name",
              "weight": 0.1,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.1, 0.3, 0.3, 0.1, 0.1, 0.1]}},
             {"name": "gender",
              "weight": 0.1,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.3, 0.3, 0.3, 0.1, 0.0, 0.0]}},
             {"name": "dob",
              "weight": 0.1,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.5, 0.3, 0.0, 0.0, 0.0, 0.2]}},
             {"name": "region",
              "weight": 0.05,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.3, 0.3, 0.2, 0.1, 0.0, 0.1]}},
             {"name": "sub_region",
              "weight": 0.05,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.3, 0.2, 0.0, 0.0, 0.2, 0.3]}},
             {"name": "phone_number",
              "weight": 0.1,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.3, 0.3, 0.2, 0.1, 0.0, 0.1]}},
             {"name": "national_id",
              "weight": 0.1,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.3, 0.3, 0.2, 0.1, 0.0, 0.1]}},
         ]}

    fields = config["fields"]
    field_name_list = []
    field_weight_list = []
    field_corruptor_name_list = {}
    field_corruptor_weight_list = {}
    for f_idx in range(len(fields)):
        field_name_list.append(fields[f_idx]['name'])
        field_weight_list.append(fields[f_idx]['weight'])
        field_corruptor_name_list[fields[f_idx]['name']] = fields[f_idx]['corruptor']['type']
        field_corruptor_weight_list[fields[f_idx]['name']] = fields[f_idx]['corruptor']['weight']

    base_date = config['BaseDate']
    seed = 123456
    rng = np.random.default_rng(seed)
    gender_generator = PatientGenerator.gender_generator(seed, 0.50)
    male_name_generator = PatientGenerator.name_generator(seed, 'metadata/name-m-freq.csv')
    female_name_generator = PatientGenerator.name_generator(seed, 'metadata/name-f-freq.csv')
    dob_generator = PatientGenerator.date_generator(seed, base_date, 'gumbel', 35, 12 * 10)
    phone_number_generator = PatientGenerator.phone_number_generator(seed, 'metadata/phone_area_codes.csv')
    town_region_generator = PatientGenerator.town_region_generator(seed, 'metadata/town-region-freq.csv')
    national_id_generator = PatientGenerator.national_id_generator(seed)
    clinical_data_generator = MinimalClinicalDataGenerator.clinical_data_generator(
        seed,
        config['AverageNumberOfClinicalRecordsPerPatient'])

    corruptor_dict = {'ocr_corruptor': Corruptors.ocr_corruptor('metadata/ocr-variations.csv', False, None,
                                                                Corruptors.position_mod_normal),
                      'missing_value_corruptor': Corruptors.missing_value_corruptor(),
                      'keyboard_corruptor': Corruptors.keyboard_corruptor(0.5, 0.5, Corruptors.position_mod_normal),
                      'edit1_corruptor': Corruptors.edit_corruptor(Corruptors.position_mod_normal,
                                                                   basefunctions.char_set_ascii,
                                                                   0.50, 0.50, 0.00, 0.00),
                      'edit2_corruptor': Corruptors.edit_corruptor(Corruptors.position_mod_uniform,
                                                                   basefunctions.char_set_ascii,
                                                                   0.25, 0.25, 0.25, 0.25),
                      'phonetic_corruptor': Corruptors.phonetic_corruptor('metadata/phonetic-variations.csv',
                                                                          False, 'utf_8')}

    number_of_patients = config.get("NumberOfPatients")
    data = []
    next(national_id_generator)
    next(phone_number_generator)
    next(clinical_data_generator)
    next(corruptor_dict['missing_value_corruptor'])
    next(corruptor_dict['ocr_corruptor'])
    next(corruptor_dict['keyboard_corruptor'])
    next(corruptor_dict['edit1_corruptor'])
    next(corruptor_dict['edit2_corruptor'])
    next(corruptor_dict['phonetic_corruptor'])
    k = 0
    for i in range(0, number_of_patients):
        k = k + 1
        if k % 1000 == 0:
            print(k)
        gender = next(gender_generator)
        given_name = next(female_name_generator)[1] if gender == 'female' else next(male_name_generator)[1]
        fathers_name = next(male_name_generator)[1]
        fathers_father_name = next(male_name_generator)[1]
        dob = next(dob_generator)
        dob = np.datetime_as_string(dob, unit='D')
        town_region = next(town_region_generator)
        phone_number = phone_number_generator.send(town_region[1])
        national_id = national_id_generator.send((dob, gender))
        clinical_data = clinical_data_generator.send((gender, base_date, dob, national_id))

        for j in range(0, len(clinical_data)):
            rec_num = "rec-%010d-%02d" % (i + 1, j)
            data.append([rec_num, given_name, fathers_name, fathers_father_name, gender, dob, town_region[1],
                         town_region[2], phone_number, national_id, clinical_data[j]])

    df = pd.DataFrame(data, columns=['rec_num', 'given_name', 'fathers_name', 'fathers_father_name', 'gender', 'dob',
                                     'region', 'sub_region', 'phone_number', 'national_id', 'clinical_data'])
    df['corrupted'] = False
    number_of_records = df.shape[0]
    percentage_of_corrupted_records = config['PercentageOfCorruptedRecords']
    number_of_corrupted_records = int(number_of_records * percentage_of_corrupted_records)
    for i in range(0, number_of_corrupted_records):
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
        print('row to corrupt: %s' % row_to_corrupt)
        for column_to_corrupt in columns_to_corrupt:
            corruptor_names = field_corruptor_name_list[column_to_corrupt]
            corruptor_weights = field_corruptor_weight_list[column_to_corrupt]
            corruptor = rng.choice(a=corruptor_names, p=corruptor_weights, size=1, replace=False)[0]
            print('col to corrupt: %s, %s' % (column_to_corrupt, corruptor))
            value_to_corrupt = df.at[row_to_corrupt, column_to_corrupt]
            corruptor_value = corruptor_dict[corruptor].send(value_to_corrupt)
            df.at[row_to_corrupt, column_to_corrupt] = corruptor_value
        print()
    df = df.drop('corrupted', axis=1)

    df.to_csv('Results/' + str(helper.generate_log_filename('synthetic_data_V')), index=False, encoding='utf-8')


def main():
    generate_dataset()


main()
