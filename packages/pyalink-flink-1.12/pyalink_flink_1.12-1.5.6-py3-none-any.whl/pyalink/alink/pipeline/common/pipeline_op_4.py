# -*- coding: utf-8 -*-

from ..base import Estimator, Transformer, Model, TuningEvaluator
from ..tuning.base import BaseGridSearch, BaseRandomSearch
from ..mixins import HasLazyPrintModelInfo, HasLazyPrintTrainInfo
from ..local_predictor import LocalPredictable
from ...common.types.bases.model_stream_scan_params import ModelStreamScanParams



class OneVsRest(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.OneVsRest'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneVsRest, self).__init__(*args, **kwargs)
        pass

    def setNumClass(self, val):
        return self._add_param('numClass', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class OneVsRestModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.OneVsRestModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneVsRestModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class OnnxModelPredictor(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.onnx.OnnxModelPredictor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OnnxModelPredictor, self).__init__(*args, **kwargs)
        pass

    def setModelPath(self, val):
        return self._add_param('modelPath', val)

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setInputNames(self, val):
        return self._add_param('inputNames', val)

    def setOutputNames(self, val):
        return self._add_param('outputNames', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)



class PCA(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.PCA'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PCA, self).__init__(*args, **kwargs)
        pass

    def setK(self, val):
        return self._add_param('k', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCalculationType(self, val):
        return self._add_param('calculationType', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class PCAModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.PCAModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PCAModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class QuantileDiscretizer(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.QuantileDiscretizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileDiscretizer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumBuckets(self, val):
        return self._add_param('numBuckets', val)

    def setNumBucketsArray(self, val):
        return self._add_param('numBucketsArray', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class QuantileDiscretizerModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.QuantileDiscretizerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileDiscretizerModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RandomForestClassificationModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.RandomForestClassificationModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestClassificationModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RandomForestClassifier(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.RandomForestClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestClassifier, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setNumTreesOfGini(self, val):
        return self._add_param('numTreesOfGini', val)

    def setNumTreesOfInfoGain(self, val):
        return self._add_param('numTreesOfInfoGain', val)

    def setNumTreesOfInfoGainRatio(self, val):
        return self._add_param('numTreesOfInfoGainRatio', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class RandomForestEncoder(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.RandomForestEncoder'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestEncoder, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setNumTreesOfGini(self, val):
        return self._add_param('numTreesOfGini', val)

    def setNumTreesOfInfoGain(self, val):
        return self._add_param('numTreesOfInfoGain', val)

    def setNumTreesOfInfoGainRatio(self, val):
        return self._add_param('numTreesOfInfoGainRatio', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class RandomForestEncoderModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.RandomForestEncoderModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestEncoderModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RandomForestRegEncoder(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.RandomForestRegEncoder'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegEncoder, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class RandomForestRegEncoderModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.RandomForestRegEncoderModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegEncoderModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RandomForestRegressionModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.RandomForestRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RandomForestRegressor(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.RandomForestRegressor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegressor, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class RandomSearchCV(BaseRandomSearch, HasLazyPrintTrainInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.RandomSearchCV'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomSearchCV, self).__init__(*args, **kwargs)
        pass

    def setNumFolds(self, val):
        return self._add_param('NumFolds', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)



class RandomSearchCVModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.RandomSearchCVModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomSearchCVModel, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)



class RandomSearchTVSplit(BaseRandomSearch, HasLazyPrintTrainInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.RandomSearchTVSplit'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomSearchTVSplit, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setTrainRatio(self, val):
        return self._add_param('trainRatio', val)



class RandomSearchTVSplitModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.RandomSearchTVSplitModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomSearchTVSplitModel, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)



class ReadAudioToTensor(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.audio.ReadAudioToTensor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ReadAudioToTensor, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRelativeFilePathCol(self, val):
        return self._add_param('relativeFilePathCol', val)

    def setRootFilePath(self, val):
        return self._add_param('rootFilePath', val)

    def setSampleRate(self, val):
        return self._add_param('sampleRate', val)

    def setDuration(self, val):
        return self._add_param('duration', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOffset(self, val):
        return self._add_param('offset', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class ReadImageToTensor(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.image.ReadImageToTensor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ReadImageToTensor, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRelativeFilePathCol(self, val):
        return self._add_param('relativeFilePathCol', val)

    def setRootFilePath(self, val):
        return self._add_param('rootFilePath', val)

    def setImageHeight(self, val):
        return self._add_param('imageHeight', val)

    def setImageWidth(self, val):
        return self._add_param('imageWidth', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RecommendationRanking(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.recommendation.RecommendationRanking'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RecommendationRanking, self).__init__(*args, **kwargs)
        pass

    def setMTableCol(self, val):
        return self._add_param('mTableCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setRankingCol(self, val):
        return self._add_param('rankingCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class RegexTokenizer(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.RegexTokenizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RegexTokenizer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setGaps(self, val):
        return self._add_param('gaps', val)

    def setMinTokenLength(self, val):
        return self._add_param('minTokenLength', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setPattern(self, val):
        return self._add_param('pattern', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setToLowerCase(self, val):
        return self._add_param('toLowerCase', val)



class RegressionTuningEvaluator(TuningEvaluator):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.RegressionTuningEvaluator'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RegressionTuningEvaluator, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setTuningRegressionMetric(self, val):
        return self._add_param('tuningRegressionMetric', val)



class RidgeRegression(Estimator, HasLazyPrintModelInfo, HasLazyPrintTrainInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.RidgeRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RidgeRegression, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)



class RidgeRegressionModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.RidgeRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RidgeRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class Segment(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.Segment'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Segment, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setUserDefinedDict(self, val):
        return self._add_param('userDefinedDict', val)



class Select(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.sql.Select'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Select, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)



class Softmax(Estimator, HasLazyPrintModelInfo, HasLazyPrintTrainInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.Softmax'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Softmax, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)



class SoftmaxModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.SoftmaxModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SoftmaxModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class StandardScaler(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.StandardScaler'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StandardScaler, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setWithMean(self, val):
        return self._add_param('withMean', val)

    def setWithStd(self, val):
        return self._add_param('withStd', val)



class StandardScalerModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.StandardScalerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StandardScalerModel, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)



class StopWordsRemover(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.StopWordsRemover'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StopWordsRemover, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setCaseSensitive(self, val):
        return self._add_param('caseSensitive', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setStopWords(self, val):
        return self._add_param('stopWords', val)



class StringApproxNearestNeighbor(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.similarity.StringApproxNearestNeighbor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StringApproxNearestNeighbor, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumBucket(self, val):
        return self._add_param('numBucket', val)

    def setNumHashTables(self, val):
        return self._add_param('numHashTables', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class StringApproxNearestNeighborModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.similarity.StringApproxNearestNeighborModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StringApproxNearestNeighborModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class StringIndexer(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.StringIndexer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StringIndexer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelName(self, val):
        return self._add_param('modelName', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setStringOrderType(self, val):
        return self._add_param('stringOrderType', val)



class StringIndexerModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.StringIndexerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StringIndexerModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class StringNearestNeighbor(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.similarity.StringNearestNeighbor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StringNearestNeighbor, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)

    def setWindowSize(self, val):
        return self._add_param('windowSize', val)



class StringNearestNeighborModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.similarity.StringNearestNeighborModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StringNearestNeighborModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class StringSimilarityPairwise(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.similarity.StringSimilarityPairwise'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StringSimilarityPairwise, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setNumBucket(self, val):
        return self._add_param('numBucket', val)

    def setNumHashTables(self, val):
        return self._add_param('numHashTables', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setWindowSize(self, val):
        return self._add_param('windowSize', val)



class SwingSimilarItemsRecommender(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.recommendation.SwingSimilarItemsRecommender'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SwingSimilarItemsRecommender, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class TF2TableModelTrainer(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.tensorflow.TF2TableModelTrainer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TF2TableModelTrainer, self).__init__(*args, **kwargs)
        pass

    def setMainScriptFile(self, val):
        return self._add_param('mainScriptFile', val)

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setUserFiles(self, val):
        return self._add_param('userFiles', val)

    def setGraphDefTag(self, val):
        return self._add_param('graphDefTag', val)

    def setInferSelectedCols(self, val):
        return self._add_param('inferSelectedCols', val)

    def setInputSignatureDefs(self, val):
        return self._add_param('inputSignatureDefs', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setOutputSignatureDefs(self, val):
        return self._add_param('outputSignatureDefs', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setSignatureDefKey(self, val):
        return self._add_param('signatureDefKey', val)

    def setUserParams(self, val):
        return self._add_param('userParams', val)



class TFSavedModelPredictor(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.tensorflow.TFSavedModelPredictor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TFSavedModelPredictor, self).__init__(*args, **kwargs)
        pass

    def setModelPath(self, val):
        return self._add_param('modelPath', val)

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setGraphDefTag(self, val):
        return self._add_param('graphDefTag', val)

    def setInputSignatureDefs(self, val):
        return self._add_param('inputSignatureDefs', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setOutputSignatureDefs(self, val):
        return self._add_param('outputSignatureDefs', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setSignatureDefKey(self, val):
        return self._add_param('signatureDefKey', val)



class TFTableModelPredictor(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.tensorflow.TFTableModelPredictor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TFTableModelPredictor, self).__init__(*args, **kwargs)
        pass

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setGraphDefTag(self, val):
        return self._add_param('graphDefTag', val)

    def setInputSignatureDefs(self, val):
        return self._add_param('inputSignatureDefs', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setOutputSignatureDefs(self, val):
        return self._add_param('outputSignatureDefs', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setSignatureDefKey(self, val):
        return self._add_param('signatureDefKey', val)



class TFTableModelTrainer(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.tensorflow.TFTableModelTrainer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TFTableModelTrainer, self).__init__(*args, **kwargs)
        pass

    def setMainScriptFile(self, val):
        return self._add_param('mainScriptFile', val)

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setUserFiles(self, val):
        return self._add_param('userFiles', val)

    def setGraphDefTag(self, val):
        return self._add_param('graphDefTag', val)

    def setInferSelectedCols(self, val):
        return self._add_param('inferSelectedCols', val)

    def setInputSignatureDefs(self, val):
        return self._add_param('inputSignatureDefs', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setOutputSignatureDefs(self, val):
        return self._add_param('outputSignatureDefs', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setSignatureDefKey(self, val):
        return self._add_param('signatureDefKey', val)

    def setUserParams(self, val):
        return self._add_param('userParams', val)



class TensorToVector(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.TensorToVector'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TensorToVector, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setConvertMethod(self, val):
        return self._add_param('convertMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class TextApproxNearestNeighbor(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.similarity.TextApproxNearestNeighbor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextApproxNearestNeighbor, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumBucket(self, val):
        return self._add_param('numBucket', val)

    def setNumHashTables(self, val):
        return self._add_param('numHashTables', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class TextApproxNearestNeighborModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.similarity.TextApproxNearestNeighborModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextApproxNearestNeighborModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class TextNearestNeighbor(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.similarity.TextNearestNeighbor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextNearestNeighbor, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)

    def setWindowSize(self, val):
        return self._add_param('windowSize', val)



class TextNearestNeighborModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.similarity.TextNearestNeighborModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextNearestNeighborModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)

