# https://towardsdatascience.com/micro-macro-weighted-averages-of-f1-score-clearly-explained-b603420b292f
import warnings
from copy import deepcopy
import json
import numpy as np

from petbenchmarks.Distance import DistanceFunction
from petreader.labels import *


def SaveJsonData(data, filename=None):
    with open(filename, 'w') as fout:
        json.dump(data, fout)
    return True


def LoadJsonData(filename):
    try:
        with open(filename, 'r') as fin:
            return json.load(fin)
    except:
        return False


class AbstractBenchmark:
    """
        Abstract class to benchmarking approaches
    """

    def __init__(self):

        #  load PET data
        self.tc = None
        #  load goldstandard data
        self.goldstandard = None
        #  store scores
        self.bench_scores = dict()

    def change_matching_strategy(self,
                                 matching_strategy: str = WORD_BASED_STRATEGY) -> None:
        """Change the matching strategy.

        Args:
            matching_strategy (str):
                it can be one of 'word-base' or 'index-based'.

        """

        # store strategy
        if matching_strategy in [WORD_BASED_STRATEGY, INDEX_BASED_STRATEGY]:
            self.matching_strategy = matching_strategy
        else:
            raise ValueError('Matching strategy {} not valid. Choose one between [{}, {}]'.format(
                    matching_strategy, WORD_BASED_STRATEGY, INDEX_BASED_STRATEGY))

    def SetMatchingFunction(self,
                            relax_window=1,
                            strategy='lr') -> None:
        self.entity_matching_relax_window = relax_window
        self.entity_matching_strategy = strategy

    @staticmethod
    def _get_data_dict_process_elements() -> dict:
        return {k: list() for k in PROCESS_ELEMENT_LABELS}

    @staticmethod
    def LoadJsonResults(json_filename: str):
        return LoadJsonData(json_filename)

    def Get_Entity_Document_level_TP_FP_TN_FN(self,
                                              goldstandard_,
                                              predictions_) -> dict:
        # warnings.warn('check this')

        #  secure copy of arrays
        goldstandard = deepcopy(goldstandard_)
        predictions = deepcopy(predictions_)

        tp = 0
        fn = 0
        fp = 0

        # try:
        # ranging over gold standard items
        for gold_item in goldstandard:
            # ranging over predicted element

            for pred_item in predictions:
                match = self.CompareItem(gold_item,
                                         pred_item)
                if match:
                    predictions.remove(pred_item)
                    tp += 1
                    break

        #  false positives are the number of elements not matched
        fp = len(predictions)

        #  false negative are the number of elements in goldstandard not predicted
        #  that is equal to the length of goldstandard not matched
        fn = len(goldstandard) - tp

        return {TRUE_POSITIVE:  tp,
                FALSE_POSITIVE: fp,
                TRUE_NEGATIVE:  0,
                FALSE_NEGATIVE: fn}

    def CompareItem(self,
                    gold,
                    pred):
        #  Compare a goldstandard item against a predicted one
        return DistanceFunction(gold,
                                pred,
                                relax_window=self.entity_matching_relax_window,
                                strategy=self.entity_matching_strategy)

    @staticmethod
    def Precision(tp, fp):
        try:
            return tp / (tp + fp)
        except ZeroDivisionError:
            return 0.0

    @staticmethod
    def Recall(tp, fn):
        try:
            return tp / (tp + fn)
        except ZeroDivisionError:
            return 0.0

    def F1(self, tp, fp, fn):
        try:
            return 2 * ((self.Precision(tp, fp) * self.Recall(tp, fn)) / (self.Precision(tp, fp) + self.Recall(tp, fn)))
        except ZeroDivisionError:
            return 0.0

    @staticmethod
    def Support(tp, fn):
        #  supports are the goldstandard items; so, the sum of tp with fn
        return tp + fn

    @staticmethod
    def round(value, decimals=2):
        #  return a raounded value of value
        return np.round(value, decimals)

    def SaveResults(self,
                    filename: str):
        #  results_data is a dict of dict containing all the results_frameworks
        SaveJsonData(self.bench_scores, filename)

    def ComputeClassEntityScores(self,
                                 golds,
                                 preds) -> dict:
        #  compute the score for Entities (token classification task) a single class
        #  golds are the goldstandard data
        #  preds are the predicted data
        if preds:
            tp_fp_tn_fn = self.Get_Entity_Document_level_TP_FP_TN_FN(golds, preds)

            tp = tp_fp_tn_fn[TRUE_POSITIVE]
            fp = tp_fp_tn_fn[FALSE_POSITIVE]
            tn = tp_fp_tn_fn[TRUE_NEGATIVE]
            fn = tp_fp_tn_fn[FALSE_NEGATIVE]
        else:
            tp = 0
            fp = 0
            tn = 0
            fn = len(golds)

        pr = self.Precision(tp=tp, fp=fp)
        rec = self.Recall(tp=tp, fn=fn)

        f1 = self.F1(tp=tp, fp=fp, fn=fn)
        supports = self.Support(tp=tp, fn=fn)

        return {TRUE_POSITIVE:  tp,
                FALSE_POSITIVE: fp,
                TRUE_NEGATIVE:  tn,
                FALSE_NEGATIVE: fn,

                PRECISION:      pr,
                RECALL:         rec,
                F1SCORE:        f1,
                SUPPORT:        supports}

    #

    def _ComputeClassScores(self,
                            scores) -> dict:
        #  compute the score for each relation class

        tp = scores[TRUE_POSITIVE]
        fp = scores[FALSE_POSITIVE]
        tn = scores[TRUE_NEGATIVE]
        fn = scores[FALSE_NEGATIVE]

        pr = self.Precision(tp=tp, fp=fp)
        rec = self.Recall(tp=tp, fn=fn)

        f1 = self.F1(tp=tp, fp=fp, fn=fn)
        supports = self.Support(tp=tp, fn=fn)

        return {TRUE_POSITIVE:  tp,
                FALSE_POSITIVE: fp,
                TRUE_NEGATIVE:  tn,
                FALSE_NEGATIVE: fn,

                PRECISION:      pr,
                RECALL:         rec,
                F1SCORE:        f1,
                SUPPORT:        supports}

    def ComputeScores(self,
                      predictions):
        raise NotImplementedError()

    def ComputeStatistics(self):
        raise NotImplementedError()

    def ShowStatistics(self):
        raise NotImplementedError()

    @staticmethod
    def print_sep(foout=None):
        sep_ = '-' * 50
        print(sep_,
              file=foout)
