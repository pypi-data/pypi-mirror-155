def DistanceFunction(gold,
                     pred,
                     relax_window=1,
                     strategy='lr'):
    #  relax_window determine the number of acepted different words at the begin of at the end of the two list
    #  strategy determine if acept a missing word:
    #               on 'l': left,
    #               'r': right,
    #               'lr: both,
    #               None: no relaxing strategy is adopted.
    ##########################################

    def strategy_l(gold, pred, aceptance_val):
        if len(gold) < len(pred):
            for q in range(1, aceptance_val+1):
                if gold == pred[q:]:
                    return True
            return False
        elif len(pred) < len(gold):
            for q in range(1, aceptance_val+1):
                if gold[q:] == pred:
                    return True
            return False
        else:
            # the two list differ
            return False
    ##########################################

    def strategy_r(gold, pred, aceptance_val):
        if len(gold) < len(pred):
            for q in range(1, aceptance_val+1):
                if gold == pred[:len(pred)-q]:
                    return True
            return False
        elif len(pred) < len(gold):
            for q in range(1, aceptance_val+1):
                if gold[:len(gold)-q] == pred:
                    return True
            return False
        else:
            # the two list differ
            return False
    ##########################################

    #  check gold and pred are list
    if type(gold) == str:
        gold = gold.strip()
        gold = gold.split(' ')
    gold = [w.lower() for w in gold]

    if type(pred) == str:
        pred = pred.strip()
        pred = pred.split(' ')
    pred = [w.lower() for w in pred]

    if gold == pred:
        return True

    else:
        if strategy:
            if strategy == 'l':
                return strategy_l(gold, pred, relax_window)
            elif strategy == 'r':
                return strategy_r(gold, pred, relax_window)
            elif strategy == 'lr':
                return strategy_l(gold, pred, relax_window) or \
                       strategy_r(gold, pred, relax_window)
        else:
            return False


if __name__ == '__main__':
    a = 'offert'
    b = 'a mortage offert'
    print('a: {}| b: {} | result: {}'.format(a, b, DistanceFunction(a, b)))
    #
    # # a sub list of b
    # a = 'is a test'
    # b = 'this is a test'
    # print('a: {}| b: {} | result: {}'.format(a, b, DistanceFunction(a, b)))
    #
    # # b sub list of a
    # a = 'this is a test'
    # b = 'this is a'
    # print('a: {}| b: {} | result: {}'.format(a, b, DistanceFunction(a, b)))
    #
    # # a != b
    # a = 'this is a test'
    # b = 'this is a goldstandard'
    # print('a: {}| b: {} | result: {}'.format(a, b, DistanceFunction(a, b)))
    #
    # a = 'this is a test'
    # b = 'this is test'
    # print('a: {}| b: {} | result: {}'.format(a, b, DistanceFunction(a, b)))
