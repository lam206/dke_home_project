def get_all_ground_truth_plds():
    sites = []
    files = ['../../../input_data/right_train.csv', '../../../input_data/left_train.csv']
    for file in files:
        with open(file, 'r') as f:
            for s in f.readlines():
                sites.append(s[:-1])
    return sites