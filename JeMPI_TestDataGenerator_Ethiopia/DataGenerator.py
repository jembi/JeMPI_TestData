import numpy as np
import pandas as pd

from Resources.ClinicalDataGenerator import MinimalClinicalDataGenerator
from Resources.DemographicDataGenerator import PatientGenerator
from Utilities import helper


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
    seed = 12345
    gender_generator = PatientGenerator.gender_generator(seed, 0.50)
    male_name_generator = PatientGenerator.name_generator(seed, 'metadata/name-m-freq.csv')
    female_name_generator = PatientGenerator.name_generator(seed, 'metadata/name-f-freq.csv')
    dob_generator = PatientGenerator.date_generator(seed, base_date, 'gumbel', 35, 12 * 10)
    phone_number_generator = PatientGenerator.phone_number_generator(seed, 'metadata/phone_area_codes.csv')
    town_region_generator = PatientGenerator.town_region_generator(seed, 'metadata/town-region-freq.csv')
    national_id_generator = PatientGenerator.national_id_generator(seed)
    clinical_data_generator = MinimalClinicalDataGenerator.clinical_data_generator(seed)
    n = 2_000
    data = []
    next(national_id_generator)
    next(phone_number_generator)
    next(clinical_data_generator)
    k = 0
    for i in range(0, n):
        k = k + 1
        if k % 1000 == 0:
            print(k)
        gender = next(gender_generator)
        name_given = next(female_name_generator)[1] if gender == 'female' else next(male_name_generator)[1]
        name_father = next(male_name_generator)[1]
        name_fathers_father = next(male_name_generator)[1]
        name_mother = next(female_name_generator)[1]
        name_mothers_father = next(male_name_generator)[1]
        dob = next(dob_generator)
        dob = np.datetime_as_string(dob, unit='D')
        town_region = next(town_region_generator)
        phone_number = phone_number_generator.send(town_region[1])
        national_id = national_id_generator.send((dob, gender))
        clinical_data = clinical_data_generator.send((gender, base_date, dob, national_id))

        for j in range(0, len(clinical_data)):
            id = "rec-%010d-%02d" % (i + 1, j)
            data.append([id, name_given, name_father, name_fathers_father, name_mother, name_mothers_father,
                         gender, dob, town_region[1], phone_number, clinical_data[j]])
    df = pd.DataFrame(data, columns=['id', 'name_given', 'name_father', 'name_fathers_father', 'name_mother',
                                     'name_mothers_father', 'gender', 'dob', 'city', 'phone_number',
                                     'clinical_data'])
    df.to_csv('Results/' + str(helper.generate_log_filename('synthetic_data_V')), index=False, encoding='utf-8')


def main():
    generate_dataset()


main()
