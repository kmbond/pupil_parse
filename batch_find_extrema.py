from pupil_parse.preprocess_utils import config as cf
from pupil_parse.preprocess_utils import extract_session_metadata as md

from pupil_parse.preprocess_utils import edf2pd as ep
from pupil_parse.preprocess_utils import visualize as vz

from pupil_parse.analysis_utils import bandpass_filter as bp

import numpy as np
import os
import pandas as pd


import time



def main():

    (raw_data_path, intermediate_data_path,
    processed_data_path, figure_path) = cf.path_config()

    valid_data_id = pd.read_csv(os.path.join(processed_data_path, 'valid_data.csv'))
    unique_subjects = valid_data_id.valid_sub.values
    unique_sessions = valid_data_id.valid_session.values


    # (unique_subjects, unique_sessions, unique_reward_codes) = md.extract_subjects_sessions(raw_data_path,
    #  reward_task=1)

    start_time = time.time()

    for subj_id in unique_subjects:
        for session_n in unique_sessions:


            print('calculating summary stats for subject {}'.format(subj_id) +
            ' session {}'.format(session_n))

            _, _, reward_code = ep.find_data_files(subj_id=subj_id,
            session_n=session_n, reward_task=1, lum_task=0,
            raw_data_path=raw_data_path)


            reward_samples = ep.read_hdf5('samples', subj_id, session_n,
            processed_data_path, reward_code=reward_code, id_str='bandpass')
            reward_messages = ep.read_hdf5('messages', subj_id, session_n,
            processed_data_path, reward_code=reward_code, id_str='bandpass')
            reward_events = ep.read_hdf5('events', subj_id, session_n,
            processed_data_path, reward_code=reward_code, id_str='bandpass')



            # for the stim onset to trial end interval ...

            # find peak amplitude
            # find peak latency
            # find fwhm
            # find area under the curve
            # calc simple average
            # calc median


    end_time = time.time()

    time_elapsed = end_time - start_time
    print('time elapsed: ', time_elapsed)

    valid_data_id = pd.DataFrame({'valid_sub': valid_subj_id,
    'valid_session': valid_session_n})

    valid_data_id.to_csv(os.path.join(processed_data_path, 'valid_data.csv'))

if __name__ == '__main__':

    main()
