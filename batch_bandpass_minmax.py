from pupil_parse.preprocess_utils import config as cf
from pupil_parse.preprocess_utils import extract_session_metadata as md

from pupil_parse.preprocess_utils import edf2pd as ep
from pupil_parse.preprocess_utils import visualize as vz

from pupil_parse.analysis_utils import bandpass_filter as bp

import numpy as np


import time


def main():

    (raw_data_path, intermediate_data_path,
    processed_data_path, figure_path) = cf.path_config()


    (unique_subjects, unique_sessions, unique_reward_codes) = md.extract_subjects_sessions(raw_data_path,
     reward_task=1)

    start_time = time.time()

    lp_min = []
    lp_max = []

    hp_min = []
    hp_max = []

    for subj_id in unique_subjects:
        for session_n in unique_sessions:

            print('bandpass filtering data for subject {}'.format(subj_id) +
            ' session {}'.format(session_n))

            _, _, reward_code = ep.find_data_files(subj_id=subj_id,
            session_n=session_n, reward_task=1, lum_task=0,
            raw_data_path=raw_data_path)


            reward_samples = ep.read_hdf5('samples', subj_id, session_n,
            processed_data_path, reward_code=reward_code, id_str='corr')
            reward_messages = ep.read_hdf5('messages', subj_id, session_n,
            processed_data_path, reward_code=reward_code, id_str='corr')
            reward_events = ep.read_hdf5('events', subj_id, session_n,
            processed_data_path, reward_code=reward_code, id_str='corr')


            reward_samples = bp.high_bandpass_filter(reward_samples)
            reward_samples = bp.low_bandpass_filter(reward_samples)

            lp_min.append(np.nanmin(reward_samples.lowpass_pupil_diameter))
            lp_max.append(np.nanmax(reward_samples.lowpass_pupil_diameter))

            hp_min.append(np.nanmin(reward_samples.highpass_pupil_diameter))
            hp_max.append(np.nanmax(reward_samples.highpass_pupil_diameter))

    end_time = time.time()

    time_elapsed = end_time - start_time
    print('time elapsed: ', time_elapsed)

    print('min lowpass values: ', np.nanmin(lp_min))
    print('max lowpass values: ', np.nanmax(lp_max))

    print('min highpass values: ', np.nanmin(hp_min))
    print('max highpass values: ', np.nanmax(hp_max))


if __name__ == '__main__':

    main()
