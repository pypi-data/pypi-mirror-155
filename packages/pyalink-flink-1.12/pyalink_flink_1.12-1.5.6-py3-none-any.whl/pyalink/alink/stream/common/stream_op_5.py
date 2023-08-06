# -*- coding: utf-8 -*-

from ..base import StreamOperator, BaseSinkStreamOp, BaseModelStreamOp
from ...common.types.bases.model_stream_scan_params import ModelStreamScanParams



class TensorFlowStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.tensorflow.TensorFlowStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TensorFlowStreamOp, self).__init__(*args, **kwargs)
        pass

    def setMainScriptFile(self, val):
        return self._add_param('mainScriptFile', val)

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setUserFiles(self, val):
        return self._add_param('userFiles', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setUserParams(self, val):
        return self._add_param('userParams', val)



class TensorToVectorStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.TensorToVectorStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TensorToVectorStreamOp, self).__init__(*args, **kwargs)
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



class TextSimilarityPairwiseStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.similarity.TextSimilarityPairwiseStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextSimilarityPairwiseStreamOp, self).__init__(*args, **kwargs)
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



class TextSinkStreamOp(BaseSinkStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sink.TextSinkStreamOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextSinkStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setNumFiles(self, val):
        return self._add_param('numFiles', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)



class TextSourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.TextSourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextSourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setIgnoreFirstLine(self, val):
        return self._add_param('ignoreFirstLine', val)

    def setPartitions(self, val):
        return self._add_param('partitions', val)

    def setTextCol(self, val):
        return self._add_param('textCol', val)



class ToMTableStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.ToMTableStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ToMTableStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class ToTensorStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.ToTensorStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ToTensorStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTensorDataType(self, val):
        return self._add_param('tensorDataType', val)

    def setTensorShape(self, val):
        return self._add_param('tensorShape', val)



class ToVectorStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.ToVectorStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ToVectorStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorType(self, val):
        return self._add_param('vectorType', val)



class TokenizerStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.nlp.TokenizerStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TokenizerStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class TorchModelPredictStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.pytorch.TorchModelPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TorchModelPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setModelPath(self, val):
        return self._add_param('modelPath', val)

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class TreeModelEncoderStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.TreeModelEncoderStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TreeModelEncoderStreamOp, self).__init__(*args, **kwargs)
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

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class TsvSinkStreamOp(BaseSinkStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sink.TsvSinkStreamOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TsvSinkStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setNumFiles(self, val):
        return self._add_param('numFiles', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)



class TsvSourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.TsvSourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TsvSourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setIgnoreFirstLine(self, val):
        return self._add_param('ignoreFirstLine', val)

    def setPartitions(self, val):
        return self._add_param('partitions', val)

    def setSkipBlankLine(self, val):
        return self._add_param('skipBlankLine', val)



class TumbleTimeWindowStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.TumbleTimeWindowStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TumbleTimeWindowStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setWindowTime(self, val):
        return self._add_param('windowTime', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setLatency(self, val):
        return self._add_param('latency', val)

    def setWatermarkType(self, val):
        return self._add_param('watermarkType', val)



class TypeConvertStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.TypeConvertStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TypeConvertStreamOp, self).__init__(*args, **kwargs)
        pass

    def setTargetType(self, val):
        return self._add_param('targetType', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)



class UnionAllStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sql.UnionAllStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UnionAllStreamOp, self).__init__(*args, **kwargs)
        pass



class UserCfItemsPerUserRecommStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.recommendation.UserCfItemsPerUserRecommStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfItemsPerUserRecommStreamOp, self).__init__(*args, **kwargs)
        pass

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setExcludeKnown(self, val):
        return self._add_param('excludeKnown', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class UserCfRateRecommStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.recommendation.UserCfRateRecommStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfRateRecommStreamOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class UserCfSimilarUsersRecommStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.recommendation.UserCfSimilarUsersRecommStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfSimilarUsersRecommStreamOp, self).__init__(*args, **kwargs)
        pass

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class UserCfUsersPerItemRecommStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.recommendation.UserCfUsersPerItemRecommStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfUsersPerItemRecommStreamOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setExcludeKnown(self, val):
        return self._add_param('excludeKnown', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorAssemblerStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorAssemblerStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorAssemblerStreamOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorBiFunctionStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorBiFunctionStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorBiFunctionStreamOp, self).__init__(*args, **kwargs)
        pass

    def setBiFuncName(self, val):
        return self._add_param('biFuncName', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorElementwiseProductStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorElementwiseProductStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorElementwiseProductStreamOp, self).__init__(*args, **kwargs)
        pass

    def setScalingVector(self, val):
        return self._add_param('scalingVector', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorFunctionStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorFunctionStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorFunctionStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFuncName(self, val):
        return self._add_param('funcName', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setWithVariable(self, val):
        return self._add_param('WithVariable', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorImputerPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorImputerPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorImputerPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)



class VectorInteractionStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorInteractionStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorInteractionStreamOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorMaxAbsScalerPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorMaxAbsScalerPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMaxAbsScalerPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)



class VectorMinMaxScalerPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorMinMaxScalerPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMinMaxScalerPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)



class VectorNormalizeStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorNormalizeStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorNormalizeStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setP(self, val):
        return self._add_param('p', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorPolynomialExpandStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorPolynomialExpandStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorPolynomialExpandStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setDegree(self, val):
        return self._add_param('degree', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorSizeHintStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorSizeHintStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorSizeHintStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setSize(self, val):
        return self._add_param('size', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorSliceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorSliceStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorSliceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setIndices(self, val):
        return self._add_param('indices', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorStandardScalerPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.vector.VectorStandardScalerPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorStandardScalerPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)



class VectorToColumnsStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.VectorToColumnsStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToColumnsStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorToCsvStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.VectorToCsvStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToCsvStreamOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorToJsonStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.VectorToJsonStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToJsonStreamOp, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorToKvStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.VectorToKvStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToKvStreamOp, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorToTensorStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.VectorToTensorStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToTensorStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTensorDataType(self, val):
        return self._add_param('tensorDataType', val)

    def setTensorShape(self, val):
        return self._add_param('tensorShape', val)



class VectorToTripleStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.format.VectorToTripleStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToTripleStreamOp, self).__init__(*args, **kwargs)
        pass

    def setTripleColumnValueSchemaStr(self, val):
        return self._add_param('tripleColumnValueSchemaStr', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class WhereStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sql.WhereStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WhereStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)



class WindowGroupByStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sql.WindowGroupByStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WindowGroupByStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectClause(self, val):
        return self._add_param('selectClause', val)

    def setSessionGap(self, val):
        return self._add_param('sessionGap', val)

    def setSlidingLength(self, val):
        return self._add_param('slidingLength', val)

    def setWindowLength(self, val):
        return self._add_param('windowLength', val)

    def setGroupByClause(self, val):
        return self._add_param('groupByClause', val)

    def setIntervalUnit(self, val):
        return self._add_param('intervalUnit', val)

    def setWindowType(self, val):
        return self._add_param('windowType', val)



class Word2VecPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.nlp.Word2VecPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Word2VecPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setPredMethod(self, val):
        return self._add_param('predMethod', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setWordDelimiter(self, val):
        return self._add_param('wordDelimiter', val)



class WriteTensorToImageStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.image.WriteTensorToImageStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WriteTensorToImageStreamOp, self).__init__(*args, **kwargs)
        pass

    def setRelativeFilePathCol(self, val):
        return self._add_param('relativeFilePathCol', val)

    def setRootFilePath(self, val):
        return self._add_param('rootFilePath', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setImageType(self, val):
        return self._add_param('imageType', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class XGBoostPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.classification.XGBoostPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(XGBoostPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class XGBoostRegPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.regression.XGBoostRegPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(XGBoostRegPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

