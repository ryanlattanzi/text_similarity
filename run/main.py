import multiprocessing
import json

import utils

CONFIG    = utils.parse_config('config.yml')
RETRY_OBJ = utils.build_retry_strategy(CONFIG['retry_limit'])

TEXT_PATH       = CONFIG['text_path']
MODEL_ENDPOINT  = CONFIG['model_endpoint']
SCORE_PRECISION = CONFIG['score_precision']

NUM_CORES = multiprocessing.cpu_count()

def process_similarity_parallel():
    text     = get_text(TEXT_PATH)
    src_text = text['src_text']
    target_text_list = text['target_text']
    parallel_inputs  = wrangle_parallel_inputs(src_text, target_text_list)
    if NUM_CORES > len(parallel_inputs):
        num_processes = len(parallel_inputs)
    else:
        num_processes = NUM_CORES
    pool = multiprocessing.Pool(processes = num_processes)
    pool.map(process_similarity_single, parallel_inputs)

def wrangle_parallel_inputs(src_text, target_text_list):
    return [{'src_text': src_text, 'target_text': t, 'precision': SCORE_PRECISION} for t in target_text_list]

def process_similarity_single(text_dict):
    text_dict['src_text']    = clean_text(text_dict['src_text'])
    text_dict['target_text'] = clean_text(text_dict['target_text'])

    try:

        resp = RETRY_OBJ.post(MODEL_ENDPOINT, json = text_dict)
        resp = resp.json()

        print('-------------------------------------------')
        print('Source:\n{}\n'.format(text_dict['src_text']))
        print('Target:\n{}\n'.format(text_dict['target_text']))

        if resp['success']:
            raw  = resp['raw_lev_distance']
            norm = resp['norm_lev_distance']
            print('Raw Levenshtein distance       : {}'.format(raw))
            print('Normalized Levenshtein distance: {0:.5f}'.format(norm))
        else:
            print('Error: {}'.format(resp['error']))
    except Exception as exc:
        print(exc)
    finally:
        print('-------------------------------------------\n')

def clean_text(text):
    # --------------------------------------------------------------------
    # THIS IS WHERE TEXT CLEANING WOULD TAKE PLACE
    # (i.e. punctuation removal, tokenization, ridding of stopwords, etc.)
    # --------------------------------------------------------------------
    return text

def get_text(text_path):
    return json.load(open(text_path, 'r'))

if __name__ == '__main__':
    process_similarity_parallel()