import flask

app = flask.Flask(__name__)

@app.route('/health', methods = ['GET'])
def check_health():
    return flask.jsonify({'status': 200})

@app.route('/similarity', methods = ['POST'])
def get_similarity():

    params = flask.request.json
    data   = {'success': False}

    src_text    = params['src_text']
    target_text = params['target_text']
    precision   = params['precision']

    src_len    = len(src_text)
    target_len = len(target_text)
    norm_len   = max([src_len, target_len])

    if not check_string_length(src_len, target_len):
        data['error'] = 'Cannot compare empty strings'
        return flask.jsonify(data)

    prev_row = [*range(0, src_len + 1, 1)]
    curr_row = [0] * (src_len + 1)

    for i in range(target_len):
        curr_row[0] = i + 1
        for j in range(src_len):
            if target_text[i] == src_text[j]:
                curr_row[j+1] = prev_row[j]
            else:
                sub    = prev_row[j]
                insert = curr_row[j]
                delete = prev_row[j+1]
                curr_row[j+1] = min([sub, insert, delete]) + 1
        prev_row = curr_row
        curr_row = [0] * (src_len + 1)

    raw_lev_distance = prev_row[src_len]

    data['raw_lev_distance']  = raw_lev_distance
    data['norm_lev_distance'] = normalize(raw_lev_distance, norm_len, precision)
    data['success'] = True

    return flask.jsonify(data)

def check_string_length(src_len, target_len):
    if (src_len == 0) or (target_len == 0):
        return False
    else:
        return True

def normalize(raw, norm_len, precision):
    return 1 - round(raw/norm_len, precision)

if __name__ == '__main__':
    app.run()