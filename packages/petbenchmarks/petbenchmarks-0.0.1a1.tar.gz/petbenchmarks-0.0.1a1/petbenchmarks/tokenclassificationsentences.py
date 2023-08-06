import codecs
import numpy as np
import warnings

from datasetreader.TokenClassification import TokenClassification
from petbenchmarks.Abstract import AbstractBenchmark
from datasetreader.labels import *


class SentenceLevelTokenClassificationBenchmark(AbstractBenchmark):
    """
        Class to benchmarking approaches on the PET dataset

    """

    def __init__(self):
        super(SentenceLevelTokenClassificationBenchmark, self).__init__()

        #  load PET data
        self.PETdataset = TokenClassification()
        #  load goldstandard data
        self.goldstandard = self.GetGoldStandard()

    def GetGoldStandard(self) -> dict:
        #  returns goldstandard entities
        return {ACTIVITY: self.PETdataset.GetActivities(),
                ACTIVITY_DATA: self.PETdataset.GetActivityData(),
                ACTOR: self.PETdataset.GetActors(),
                FURTHER_SPECIFICATION: self.PETdataset.GetFurtherSpecifications(),
                XOR_GATEWAY: self.PETdataset.GetXORGateways(),
                AND_GATEWAY: self.PETdataset.GetANDGateways(),
                CONDITION_SPECIFICATION: self.PETdataset.GetConditionSpecifications()}

    def ComputeScores(self,
                      predictions):

        for k in PROCESS_ELEMENT_LABELS:
            #  check that the lengths are equal
            if len(self.goldstandard[k]) != len(predictions[k]):

                warnings.warn(
                    "Predictions size error in class ''{}''. Expected {} found {}".format(k,
                                                                                          len(self.goldstandard[k]),
                                                                                          len(predictions[k])))
            else:
                #  do comparison

                golds = self.goldstandard[k]
                preds = predictions[k]
                #  get class scores
                scores = self.ComputeClassEntityScores(golds, preds)
                #  add class label to scores
                scores['class'] = k
                #  add results_frameworks to global results_frameworks
                self.bench_scores[k] = scores


    def ComputeStatistics(self):
        #  compute global statistics
        supports_statistics = self.Supports(self.bench_scores)
        micro_statistics = self.__MicroStatistics(self.bench_scores)
        macro_statistics = self.__MacroStatisctics(self.bench_scores)
        average_statistics = self.__AverageStatistics(self.bench_scores)

        self.bench_scores.update(supports_statistics)
        self.bench_scores.update(micro_statistics)
        self.bench_scores.update(macro_statistics)
        self.bench_scores.update(average_statistics)

    @staticmethod
    def Supports(results: dict) -> dict:
        #  return a dict with the sum of supports
        #  it returns a dict to conform with the other statistics methods
        return {SUPPORT: int(np.sum([results[k][SUPPORT] for k in results]))}

    @staticmethod
    def __MacroStatisctics(results: dict) -> dict:
        #  results_frameworks a dict of the global results_frameworks

        #  The macro-averaged F1 score (or macro F1 score) is computed by taking
        #  the arithmetic mean (aka unweighted mean) of all the per-class F1 scores.
        macro_precision = np.mean([results[k][PRECISION] for k in results])
        macro_recall = np.mean([results[k][RECALL] for k in results])
        macro_f1 = np.mean([results[k][F1SCORE] for k in results])

        return {MACRO_PRECISION: macro_precision,
                MACRO_RECALL: macro_recall,
                MACRO_F1SCORE: macro_f1}

    @staticmethod
    def __AverageStatistics(results: dict) -> dict:
        # results_frameworks a dict of the global results_frameworks

        #  The weighted-averaged F1 score is calculated by taking the mean of all per-class
        #  F1 scores while considering each class’s support.

        precisions = [results[k][PRECISION] for k in results]
        recalls = [results[k][RECALL] for k in results]
        f1s = [results[k][F1SCORE] for k in results]
        supports = [results[k][SUPPORT] for k in results]

        average_precision = np.average(precisions, weights=supports)
        average_recall = np.average(recalls, weights=supports)
        average_f1 = np.average(f1s, weights=supports)

        return {AVERAGE_PRECISION: average_precision,
                AVERAGE_RECALL: average_recall,
                AVERAGE_F1SCORE: average_f1}

    def __MicroStatistics(self, results: dict) -> dict:
        #  results_frameworks a dict of the global results_frameworks

        # Micro averaging computes a global average F1 score by counting the sums of the True Positives (TP),
        # False Negatives (FN), and False Positives (FP).

        tps = [results[k][TRUE_POSITIVE] for k in results]
        TP = np.sum(tps)
        fps = [results[k][FALSE_POSITIVE] for k in results]
        FP = np.sum(fps)
        fns = [results[k][FALSE_NEGATIVE] for k in results]
        FN = np.sum(fns)

        micro_precision = self.Precision(tp=TP, fp=FP)
        micro_recall = self.Recall(tp=TP, fn=FN)
        micro_f1 = self.F1(TP, FP, FN)

        return {MICRO_PRECISION: micro_precision,
                MICRO_RECALL: micro_recall,
                MICRO_F1SCORE: micro_f1}

    def __ShowItemStatistics(self,
                             results: dict,
                             foout=None) -> None:
        #  results_frameworks is a dict with class results_frameworks
        print('{class_:<25} precision: {pr:1.2f} | recall: {rec:1.2f} | f1: {f1:1.2f} | supports: {sup:n}'.format(
            class_=results['class'],
            pr=self.round(results[PRECISION]),
            rec=self.round(results[RECALL]),
            f1=self.round(results[F1SCORE]),
            sup=results[SUPPORT]),
            file=foout)

    def ShowStatistics(self,
                       filename=None):
        if filename:
            #  save results onto file
            foout = codecs.open(filename, 'w', 'utf-8')
        else:
            foout = None

        results = self.bench_scores
        #  show the overall results_frameworks of the framework compared
        #  results_frameworks is a dict with all the data collected
        for k in PROCESS_ELEMENT_LABELS:
            self.__ShowItemStatistics(results[k],
                                      foout)

        print('',
              file=foout)
        print('Overall statistics',
              file=foout)
        print('{class_:<25} precision: {pr:1.2f} | recall: {rec:1.2f} | f1: {f1:1.2f}'.format(
            class_=MACRO_STATISTICS,
            pr=self.round(results[MACRO_PRECISION]),
            rec=self.round(results[MACRO_RECALL]),
            f1=self.round(results[MACRO_F1SCORE])),
            file=foout)

        print('{class_:<25} precision: {pr:1.2f} | recall: {rec:1.2f} | f1: {f1:1.2f}'.format(
            class_=AVERAGE_STATISTICS,
            pr=self.round(results[AVERAGE_PRECISION]),
            rec=self.round(results[AVERAGE_RECALL]),
            f1=self.round(results[AVERAGE_F1SCORE])),
            file=foout)
        print('{class_:<25} precision: {pr:1.2f} | recall: {rec:1.2f} | f1: {f1:1.2f}'.format(
            class_=MICRO_STATISTICS,
            pr=self.round(results[MICRO_PRECISION]),
            rec=self.round(results[MICRO_RECALL]),
            f1=self.round(results[MICRO_F1SCORE])),
            file=foout)

        print('Supports: {}'.format(results[SUPPORT]),
              file=foout)

        #  close file
        if foout:
            foout.close()

if __name__ == '__main__':
    bench = SentenceLevelTokenClassificationBenchmark()
    # results = bench.ComputeScores()
    # bench.ShowStatistics(results)
    # bench.SaveResults(results, 'test-results_frameworks.json')
    # with codecs.open('test bench token sentence', 'w', 'utf-8') as foout:
    #     bench.ShowStatistics(results, foout)
