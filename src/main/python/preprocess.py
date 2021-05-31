def get_set_of_websites(file):
    sites = set()
    with open(file, 'r') as f:
        for s in f.readlines():
            sites.add(s[:-1])
    return sites

sites = get_set_of_websites('../../../input_data/left_train.csv')
print('readingthepictures.org' in sites)