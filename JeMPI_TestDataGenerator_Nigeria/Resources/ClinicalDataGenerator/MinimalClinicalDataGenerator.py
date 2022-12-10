import base64
import hashlib
from collections.abc import Generator

import numpy as np
from Crypto.Cipher import AES


def get_private_key(password):
    return hashlib.sha256(password.encode()).digest()


def encrypt(clear_text, key, emr):
    cipher = AES.new(key, AES.MODE_GCM, emr.encode('utf-8'))
    cipher_text = cipher.encrypt(bytes(clear_text, 'utf-8'))
    # print(cipher_text.hex())
    return base64.b64encode(cipher_text).decode('ascii')


def decrypt(cipher_text, key, emr):
    enc = base64.b64decode(cipher_text)
    cipher = AES.new(key, AES.MODE_GCM, emr.encode('utf-8'))
    return cipher.decrypt(enc)


def encode_finger_print(key, emr, finger_print):
    encoded_finger_print = encrypt(str(int(finger_print)), key, emr)
    # print(str(int(finger_print)) +
    #       " -> " + encoded_finger_print +
    #       " -> " + str(decrypt(encoded_finger_print, key, emr)))
    return encoded_finger_print


def get_clinical_fields(key, emr, p_id, fp_id):
    return [emr, p_id, encode_finger_print(key, emr, fp_id)]


def clinical_data_generator(seed, average_number_of_clinical_records_per_patient) -> Generator[
    (str, str, str), (str, str), None]:
    """
    Random source id generator

    Args:
        seed: random national_id generator's seed.
        average_number_of_clinical_records_per_patient:

    Returns:
        yields a source id tuple

    """
    emr_list = ['EMR1', 'EMR2', 'EMR3', 'EMR4', 'EMR5']
    rng = np.random.default_rng(seed)
    key_dict = {'EMR1': get_private_key('EMR1'),
                'EMR2': get_private_key('EMR2'),
                'EMR3': get_private_key('EMR3'),
                'EMR4': get_private_key('EMR4'),
                'EMR5': get_private_key('EMR5')}

    y = []
    while True:
        yield y
        _dummy_patient_id = rng.integers(100_000_000, 999_999_999)
        _dummy_finger_print = rng.integers(1_000_000_000, 9_999_999_999)
        emr_visits = rng.choice(emr_list,
                                rng.integers(1, average_number_of_clinical_records_per_patient * 2),
                                p=[0.2, 0.2, 0.2, 0.2, 0.2])
        y = [get_clinical_fields(key_dict.get(emr),
                                 emr,
                                 hashlib.sha1((emr + str(_dummy_patient_id)).encode('utf-8')).hexdigest(),
                                 _dummy_finger_print) for emr in emr_visits]
