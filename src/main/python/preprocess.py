def get_set_of_websites(file):
    sites = set()
    with open(file, 'r') as f:
        for s in f.readlines():
            sites.add(s[:-1])
    return sites


def make_regex(file):
    sites = get_set_of_websites(file)
    regex = ''
    for site in sites:
        regex += '(' + site + ')|'
    return regex[:-1]  # don't include final '|'


regex = make_regex('../../../input_data/right_train.csv')
with open('../../../input_data/right_train_regex.csv', 'w') as f:
    f.write(regex)
