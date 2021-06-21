def get_all_ground_truth_plds():
    sites = []
    files = ['../../../input_data/right_train.csv', '../../../input_data/left_train.csv']
    for file in files:
        with open(file, 'r') as f:
            for s in f.readlines():
                sites.append(s[:-1])
    return sites

def get_left_ground_truth_plds():
    sites = []
    file = '../../../input_data/left_train.csv'
    with open(file, 'r') as f:
        for s in f.readlines():
            sites.append(s[:-1])
    return sites

def get_right_ground_truth_plds():
    sites = []
    file = '../../../input_data/right_train.csv'
    with open(file, 'r') as f:
        for s in f.readlines():
            sites.append(s[:-1])
    return sites

def get_plds_from_file(filepath):
    sites = []
    with open(filepath, 'r') as f:
        for s in f.readlines():
            sites.append(s[:-1])
    return sites