import numpy as np
import pandas as pd

from Resources.ClinicalDataGenerator import MinimalClinicalDataGenerator
from Resources.CorruptorGenerator import Corruptors
from Resources.DemographicDataGenerator import PatientGenerator
from Utilities import helper, basefunctions


def generate_dataset_min():
    config = \
        {"BaseDate": "2022-01-01",
         "NumberOfPatients": 1_000,
         "AverageNumberOfClinicalRecordsPerPatient": 10,
         "PercentageOfCorruptedRecords": 0.8,
         "fields": [
             {"name": "gender",
              "weight": 0.5,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.3, 0.3, 0.3, 0.1, 0.0, 0.0]}},
             {"name": "dob",
              "weight": 0.5,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.5, 0.3, 0.0, 0.0, 0.0, 0.2]}},
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
    dob_generator = PatientGenerator.date_generator(seed, base_date, 'gumbel', 35, 12 * 10)
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
    # next(national_id_generator)
    # next(phone_number_generator)
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
        # given_name = next(female_name_generator)[1] if gender == 'female' else next(male_name_generator)[1]
        # family_name = next(family_name_generator)[1]
        dob = next(dob_generator)
        dob = np.datetime_as_string(dob, unit='D')
        # city = next(city_generator)[1]
        # phone_number = phone_number_generator.send(city)
        # national_id = national_id_generator.send((dob, gender))
        clinical_data = clinical_data_generator.send(())
        # print(clinical_data)

        for j in range(0, len(clinical_data)):
            rec_num = "rec-%010d-%02d" % (i + 1, j)
            data.append([rec_num, gender, dob,
                         clinical_data[j][0], clinical_data[j][1], clinical_data[j][2]])

    df = pd.DataFrame(data, columns=['rec_num', 'gender', 'dob', 'emr', 'p_id', 'f_id'])
    number_of_records = df.shape[0]
    percentage_of_corrupted_records = config['PercentageOfCorruptedRecords']
    number_of_corrupted_records = int(number_of_records * percentage_of_corrupted_records)
    rows_to_corrupt = rng.choice(a=number_of_records,
                                 size=number_of_corrupted_records,
                                 replace=False)
    i = 0
    for row_to_corrupt in rows_to_corrupt:
        i = i + 1
        if i % 100 == 0:
            print("corrupting row %d of %d --- row %d" % (i, number_of_corrupted_records, row_to_corrupt))
        columns_to_corrupt = rng.choice(a=field_name_list,
                                        p=field_weight_list,
                                        size=rng.integers(1, len(field_weight_list) + 1),
                                        replace=False)
        for column_to_corrupt in columns_to_corrupt:
            corruptor_names = field_corruptor_name_list[column_to_corrupt]
            corruptor_weights = field_corruptor_weight_list[column_to_corrupt]
            corruptor = rng.choice(a=corruptor_names, p=corruptor_weights, size=1, replace=False)[0]
            value_to_corrupt = df.at[row_to_corrupt, column_to_corrupt]
            corruptor_value = corruptor_dict[corruptor].send(value_to_corrupt)
            df.at[row_to_corrupt, column_to_corrupt] = corruptor_value

    df.to_csv('Results/' + str(helper.generate_log_filename('synthetic_data_min_V')), index=False, encoding='utf-8')

def generate_dataset_example():
    config = \
        {"BaseDate": "2022-01-01",
         "NumberOfPatients": 1_000,
         "AverageNumberOfClinicalRecordsPerPatient": 10,
         "PercentageOfCorruptedRecords": 0.8,
         "fields": [
             {"name": "gender",
              "weight": 0.2,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.3, 0.3, 0.3, 0.1, 0.0, 0.0]}},
             {"name": "dob",
              "weight": 0.5,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.5, 0.3, 0.0, 0.0, 0.0, 0.2]}},
             {"name": "city",
              "weight": 0.3,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.3, 0.3, 0.2, 0.1, 0.0, 0.1]}}
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
    dob_generator = PatientGenerator.date_generator(seed, base_date, 'gumbel', 35, 12 * 10)
    city_generator = PatientGenerator.city_generator(seed, 'metadata/city-freq.csv')
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
        # given_name = next(female_name_generator)[1] if gender == 'female' else next(male_name_generator)[1]
        # family_name = next(family_name_generator)[1]
        dob = next(dob_generator)
        dob = np.datetime_as_string(dob, unit='D')
        city = next(city_generator)[1]
        # phone_number = phone_number_generator.send(city)
        # national_id = national_id_generator.send((dob, gender))
        clinical_data = clinical_data_generator.send(())
        # print(clinical_data)

        for j in range(0, len(clinical_data)):
            rec_num = "rec-%010d-%02d" % (i + 1, j)
            data.append([rec_num, gender, dob, city,
                         clinical_data[j][0], clinical_data[j][1], clinical_data[j][2]])

    df = pd.DataFrame(data, columns=['rec_num', 'gender', 'dob', 'city', 'emr', 'p_id', 'f_id'])
    number_of_records = df.shape[0]
    percentage_of_corrupted_records = config['PercentageOfCorruptedRecords']
    number_of_corrupted_records = int(number_of_records * percentage_of_corrupted_records)
    rows_to_corrupt = rng.choice(a=number_of_records,
                                 size=number_of_corrupted_records,
                                 replace=False)
    i = 0
    for row_to_corrupt in rows_to_corrupt:
        i = i + 1
        if i % 100 == 0:
            print("corrupting row %d of %d --- row %d" % (i, number_of_corrupted_records, row_to_corrupt))
        columns_to_corrupt = rng.choice(a=field_name_list,
                                        p=field_weight_list,
                                        size=rng.integers(1, len(field_weight_list) + 1),
                                        replace=False)
        for column_to_corrupt in columns_to_corrupt:
            corruptor_names = field_corruptor_name_list[column_to_corrupt]
            corruptor_weights = field_corruptor_weight_list[column_to_corrupt]
            corruptor = rng.choice(a=corruptor_names, p=corruptor_weights, size=1, replace=False)[0]
            value_to_corrupt = df.at[row_to_corrupt, column_to_corrupt]
            corruptor_value = corruptor_dict[corruptor].send(value_to_corrupt)
            df.at[row_to_corrupt, column_to_corrupt] = corruptor_value

    df.to_csv('Results/' + str(helper.generate_log_filename('synthetic_data_example_V')), index=False, encoding='utf-8')

def generate_dataset_full():
    config = \
        {"BaseDate": "2022-01-01",
         "NumberOfPatients": 1_000,
         "AverageNumberOfClinicalRecordsPerPatient": 10,
         "PercentageOfCorruptedRecords": 0.8,
         "fields": [
             {"name": "given_name",
              "weight": 0.2,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.2, 0.2, 0.2, 0.1, 0.15, 0.15]}},
             {"name": "family_name",
              "weight": 0.2,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.2, 0.3, 0.1, 0.1, 0.1, 0.2]}},
             {"name": "gender",
              "weight": 0.1,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.3, 0.3, 0.3, 0.1, 0.0, 0.0]}},
             {"name": "dob",
              "weight": 0.2,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.5, 0.3, 0.0, 0.0, 0.0, 0.2]}},
             {"name": "city",
              "weight": 0.1,
              "corruptor": {
                  "type": ["missing_value_corruptor", "keyboard_corruptor", "edit1_corruptor", "edit2_corruptor",
                           "phonetic_corruptor", "ocr_corruptor"],
                  "weight": [0.3, 0.3, 0.2, 0.1, 0.0, 0.1]}},
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
    family_name_generator = PatientGenerator.name_generator(seed, 'metadata/family-name-freq.csv')
    dob_generator = PatientGenerator.date_generator(seed, base_date, 'gumbel', 35, 12 * 10)
    phone_number_generator = PatientGenerator.phone_number_generator(seed, 'metadata/phone_area_codes.csv')
    city_generator = PatientGenerator.city_generator(seed, 'metadata/city-freq.csv')
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
        family_name = next(family_name_generator)[1]
        dob = next(dob_generator)
        dob = np.datetime_as_string(dob, unit='D')
        city = next(city_generator)[1]
        phone_number = phone_number_generator.send(city)
        national_id = national_id_generator.send((dob, gender))
        clinical_data = clinical_data_generator.send(())
        # print(clinical_data)

        for j in range(0, len(clinical_data)):
            rec_num = "rec-%010d-%02d" % (i + 1, j)
            data.append([rec_num, given_name, family_name, gender, dob, city,
                         phone_number, national_id,
                         clinical_data[j][0], clinical_data[j][1], clinical_data[j][2]])

    df = pd.DataFrame(data, columns=['rec_num', 'given_name', 'family_name', 'gender', 'dob',
                                     'city', 'phone_number', 'national_id', 'emr', 'p_id', 'f_id'])
    number_of_records = df.shape[0]
    percentage_of_corrupted_records = config['PercentageOfCorruptedRecords']
    number_of_corrupted_records = int(number_of_records * percentage_of_corrupted_records)
    rows_to_corrupt = rng.choice(a=number_of_records,
                                 size=number_of_corrupted_records,
                                 replace=False)
    i = 0
    for row_to_corrupt in rows_to_corrupt:
        i = i + 1
        if i % 100 == 0:
            print("corrupting row %d of %d --- row %d" % (i, number_of_corrupted_records, row_to_corrupt))
        columns_to_corrupt = rng.choice(a=field_name_list,
                                        p=field_weight_list,
                                        size=rng.integers(1, len(field_weight_list) + 1),
                                        replace=False)
        for column_to_corrupt in columns_to_corrupt:
            corruptor_names = field_corruptor_name_list[column_to_corrupt]
            corruptor_weights = field_corruptor_weight_list[column_to_corrupt]
            corruptor = rng.choice(a=corruptor_names, p=corruptor_weights, size=1, replace=False)[0]
            value_to_corrupt = df.at[row_to_corrupt, column_to_corrupt]
            corruptor_value = corruptor_dict[corruptor].send(value_to_corrupt)
            df.at[row_to_corrupt, column_to_corrupt] = corruptor_value

    df.to_csv('Results/' + str(helper.generate_log_filename('synthetic_data_full_V')), index=False, encoding='utf-8')


def main():
    generate_dataset_example()


main()
