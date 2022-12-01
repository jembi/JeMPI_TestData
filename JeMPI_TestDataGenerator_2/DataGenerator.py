import numpy as np
import pandas as pd

from Resources.ClinicalDataGenerator import MinimalClinicalDataGenerator
from Resources.CorruptorGenerator import Corruptors
from Resources.DemographicDataGenerator import PatientGenerator
from Utilities import helper, basefunctions


def generate_dataset():
    base_date = '2022-01-01'
    seed = 12345
    gender_generator = PatientGenerator.gender_generator(seed, 0.50)
    male_name_generator = PatientGenerator.name_generator(seed, 'metadata/name-m-freq.csv')
    female_name_generator = PatientGenerator.name_generator(seed, 'metadata/name-f-freq.csv')
    dob_generator = PatientGenerator.date_generator(seed, base_date, 'gumbel', 35, 12 * 10)
    phone_number_generator = PatientGenerator.phone_number_generator(seed, 'metadata/phone_area_codes.csv')
    town_region_generator = PatientGenerator.town_region_generator(seed, 'metadata/town-region-freq.csv')
    national_id_generator = PatientGenerator.national_id_generator(seed)
    clinical_data_generator = MinimalClinicalDataGenerator.clinical_data_generator(seed)
    all_upper_case_corruptor = Corruptors.all_upper_case_corruptor()
    ocr_corruptor = Corruptors.ocr_corruptor('metadata/ocr-variations.csv', False, None, Corruptors.position_mod_normal)
    missing_value_corruptor = Corruptors.missing_value_corruptor()
    keyboard_corruptor = Corruptors.keyboard_corruptor(0.5, 0.5, Corruptors.position_mod_normal)
    edit1_corruptor = Corruptors.edit_corruptor(Corruptors.position_mod_normal, basefunctions.char_set_ascii,
                                                0.50, 0.50, 0.00, 0.00)
    edit2_corruptor = Corruptors.edit_corruptor(Corruptors.position_mod_uniform, basefunctions.char_set_ascii, 
                                                0.25, 0.25, 0.25, 0.25)
    phonetic_corruptor = Corruptors.phonetic_corruptor('metadata/phonetic-variations.csv', False, 'utf_8')

    n = 10
    data = []
    next(national_id_generator)
    next(phone_number_generator)
    next(clinical_data_generator)
    next(all_upper_case_corruptor)
    next(missing_value_corruptor)
    next(ocr_corruptor)
    next(keyboard_corruptor)
    next(edit1_corruptor)
    next(edit2_corruptor)
    next(phonetic_corruptor)
    k = 0
    for i in range(0, n):
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

    # for required number of corrupted row
    #   select the row
    #   select the columnS to corrupt
    #   for each column to corrupt
    #     select corruptor and apply

    df['gender'][1] = all_upper_case_corruptor.send(df['gender'][1])
    df['gender'][3] = missing_value_corruptor.send(df['gender'][3])

    row = 5
    df['given_name'][row] = ocr_corruptor.send(df['given_name'][row])
    df['fathers_name'][row] = ocr_corruptor.send(df['fathers_name'][row])
    df['fathers_father_name'][row] = ocr_corruptor.send(df['fathers_father_name'][row])
    df['gender'][row] = ocr_corruptor.send(df['gender'][row])
    df['dob'][row] = ocr_corruptor.send(df['dob'][row])
    df['region'][row] = ocr_corruptor.send(df['region'][row])
    df['sub_region'][row] = ocr_corruptor.send(df['sub_region'][row])
    df['phone_number'][row] = ocr_corruptor.send(df['phone_number'][row])
    df['national_id'][row] = ocr_corruptor.send(df['national_id'][row])

    row = 6
    df['given_name'][row] = keyboard_corruptor.send(df['given_name'][row])
    df['fathers_name'][row] = keyboard_corruptor.send(df['fathers_name'][row])
    df['fathers_father_name'][row] = keyboard_corruptor.send(df['fathers_father_name'][row])
    df['gender'][row] = keyboard_corruptor.send(df['gender'][row])
    df['dob'][row] = keyboard_corruptor.send(df['dob'][row])
    df['region'][row] = keyboard_corruptor.send(df['region'][row])
    df['sub_region'][row] = keyboard_corruptor.send(df['sub_region'][row])
    df['phone_number'][row] = keyboard_corruptor.send(df['phone_number'][row])
    df['national_id'][row] = keyboard_corruptor.send(df['national_id'][row])

    row = 7
    df['given_name'][row] = edit1_corruptor.send(df['given_name'][row])
    df['fathers_name'][row] = edit1_corruptor.send(df['fathers_name'][row])
    df['fathers_father_name'][row] = edit1_corruptor.send(df['fathers_father_name'][row])
    df['gender'][row] = edit1_corruptor.send(df['gender'][row])
    # df['dob'][row] = edit1_corruptor.send(df['dob'][row])
    df['region'][row] = edit1_corruptor.send(df['region'][row])
    df['sub_region'][row] = edit1_corruptor.send(df['sub_region'][row])
    df['phone_number'][row] = edit1_corruptor.send(df['phone_number'][row])
    df['national_id'][row] = edit1_corruptor.send(df['national_id'][row])

    row = 8
    df['given_name'][row] = edit2_corruptor.send(df['given_name'][row])
    df['fathers_name'][row] = edit2_corruptor.send(df['fathers_name'][row])
    df['fathers_father_name'][row] = edit2_corruptor.send(df['fathers_father_name'][row])
    df['gender'][row] = edit2_corruptor.send(df['gender'][row])
    # df['dob'][row] = edit2_corruptor.send(df['dob'][row])
    df['region'][row] = edit2_corruptor.send(df['region'][row])
    df['sub_region'][row] = edit2_corruptor.send(df['sub_region'][row])
    df['phone_number'][row] = edit2_corruptor.send(df['phone_number'][row])
    df['national_id'][row] = edit2_corruptor.send(df['national_id'][row])

    row = 9
    df['given_name'][row] = phonetic_corruptor.send(df['given_name'][row])
    df['fathers_name'][row] = phonetic_corruptor.send(df['fathers_name'][row])
    df['fathers_father_name'][row] = phonetic_corruptor.send(df['fathers_father_name'][row])
    df['gender'][row] = phonetic_corruptor.send(df['gender'][row])
    df['dob'][row] = phonetic_corruptor.send(df['dob'][row])
    df['region'][row] = phonetic_corruptor.send(df['region'][row])
    df['sub_region'][row] = phonetic_corruptor.send(df['sub_region'][row])
    df['phone_number'][row] = phonetic_corruptor.send(df['phone_number'][row])
    df['national_id'][row] = phonetic_corruptor.send(df['national_id'][row])


    df.to_csv('Results/' + str(helper.generate_log_filename('synthetic_data_V')), index=False, encoding='utf-8')


def main():
    generate_dataset()


main()
