__all__ = [
    'fpgrowth',
]

def fpgrowth(seq, **kwargs):
    import pyfpgrowth
    sup = int(kwargs.pop('sup'))
    conf = float(kwargs.pop('conf'))
    patterns = pyfpgrowth.find_frequent_patterns(seq, sup)
    rules = pyfpgrowth.generate_association_rules(patterns, conf)
    ret = [[key, value[0], value[1]] for key, value in rules.items()]
    return ret




