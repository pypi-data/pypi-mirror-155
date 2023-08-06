# -*- coding: utf-8 -*-

from ..base import StreamOperator, BaseSinkStreamOp, BaseModelStreamOp
from ...common.types.bases.model_stream_scan_params import ModelStreamScanParams



class OcsvmOutlierStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.outlier.OcsvmOutlierStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OcsvmOutlierStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPrecedingTime(self, val):
        return self._add_param('precedingTime', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCoef0(self, val):
        return self._add_param('coef0', val)

    def setDegree(self, val):
        return self._add_param('degree', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setKernelType(self, val):
        return self._add_param('kernelType', val)

    def setNu(self, val):
        return self._add_param('nu', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setPrecedingRows(self, val):
        return self._add_param('precedingRows', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class OneHotPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.OneHotPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneHotPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class OnlineFmModelFilterStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.onlinelearning.OnlineFmModelFilterStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OnlineFmModelFilterStreamOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setAccuracyThreshold(self, val):
        return self._add_param('accuracyThreshold', val)

    def setAucThreshold(self, val):
        return self._add_param('aucThreshold', val)

    def setLogLoss(self, val):
        return self._add_param('logLoss', val)

    def setPositiveLabelValueString(self, val):
        return self._add_param('positiveLabelValueString', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class OnlineFmTrainStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.onlinelearning.OnlineFmTrainStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OnlineFmTrainStreamOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBeta(self, val):
        return self._add_param('beta', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setLambda0(self, val):
        return self._add_param('lambda0', val)

    def setLambda1(self, val):
        return self._add_param('lambda1', val)

    def setLambda2(self, val):
        return self._add_param('lambda2', val)

    def setMiniBatchSize(self, val):
        return self._add_param('miniBatchSize', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumFactor(self, val):
        return self._add_param('numFactor', val)

    def setTimeInterval(self, val):
        return self._add_param('timeInterval', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setWithLinearItem(self, val):
        return self._add_param('withLinearItem', val)



class OnnxModelPredictStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.onnx.OnnxModelPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OnnxModelPredictStreamOp, self).__init__(*args, **kwargs)
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



class OverCountWindowStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.OverCountWindowStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OverCountWindowStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setLatency(self, val):
        return self._add_param('latency', val)

    def setPrecedingRows(self, val):
        return self._add_param('precedingRows', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setWatermarkType(self, val):
        return self._add_param('watermarkType', val)



class OverTimeWindowStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.OverTimeWindowStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OverTimeWindowStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

    def setPrecedingTime(self, val):
        return self._add_param('precedingTime', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setLatency(self, val):
        return self._add_param('latency', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setWatermarkType(self, val):
        return self._add_param('watermarkType', val)



class ParquetSourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.ParquetSourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ParquetSourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setPartitions(self, val):
        return self._add_param('partitions', val)



class PcaPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.PcaPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PcaPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class PipelinePredictStreamOp(StreamOperator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.PipelineModel$PipelinePredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PipelinePredictStreamOp, self).__init__(*args, **kwargs)
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



class PrintStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.utils.PrintStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PrintStreamOp, self).__init__(*args, **kwargs)
        pass

    def setMaxLimit(self, val):
        return self._add_param('maxLimit', val)

    def setRefreshInterval(self, val):
        return self._add_param('refreshInterval', val)



class ProphetPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.timeseries.ProphetPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ProphetPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

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

    def setPredictNum(self, val):
        return self._add_param('predictNum', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class ProphetStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.timeseries.ProphetStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ProphetStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictNum(self, val):
        return self._add_param('predictNum', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setStanInit(self, val):
        return self._add_param('stanInit', val)

    def setUncertaintySamples(self, val):
        return self._add_param('uncertaintySamples', val)



class PyScalarFnStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.utils.PyScalarFnStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PyScalarFnStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClassObject(self, val):
        return self._add_param('classObject', val)

    def setClassObjectType(self, val):
        return self._add_param('classObjectType', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setResultType(self, val):
        return self._add_param('resultType', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setPythonVersion(self, val):
        return self._add_param('pythonVersion', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class PySqlCmdStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sql.PySqlCmdStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PySqlCmdStreamOp, self).__init__(*args, **kwargs)
        pass

    def setCommand(self, val):
        return self._add_param('command', val)



class PyTableFnStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.utils.PyTableFnStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PyTableFnStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClassObject(self, val):
        return self._add_param('classObject', val)

    def setClassObjectType(self, val):
        return self._add_param('classObjectType', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setResultTypes(self, val):
        return self._add_param('resultTypes', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setPythonVersion(self, val):
        return self._add_param('pythonVersion', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class QuantileDiscretizerPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.QuantileDiscretizerPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileDiscretizerPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RandomForestPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.classification.RandomForestPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RandomForestRegPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.regression.RandomForestRegPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegPredictStreamOp, self).__init__(*args, **kwargs)
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



class RandomTableSourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.RandomTableSourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomTableSourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setMaxRows(self, val):
        return self._add_param('maxRows', val)

    def setNumCols(self, val):
        return self._add_param('numCols', val)

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setOutputColConfs(self, val):
        return self._add_param('outputColConfs', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setTimePerSample(self, val):
        return self._add_param('timePerSample', val)

    def setTimeZones(self, val):
        return self._add_param('timeZones', val)



class RandomVectorSourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.RandomVectorSourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomVectorSourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setMaxRows(self, val):
        return self._add_param('maxRows', val)

    def setSize(self, val):
        return self._add_param('size', val)

    def setSparsity(self, val):
        return self._add_param('sparsity', val)

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setTimePerSample(self, val):
        return self._add_param('timePerSample', val)



class ReadAudioToTensorStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.audio.ReadAudioToTensorStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ReadAudioToTensorStreamOp, self).__init__(*args, **kwargs)
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



class ReadImageToTensorStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.image.ReadImageToTensorStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ReadImageToTensorStreamOp, self).__init__(*args, **kwargs)
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



class RecommendationRankingStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.recommendation.RecommendationRankingStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RecommendationRankingStreamOp, self).__init__(*args, **kwargs)
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

    def setRankingCol(self, val):
        return self._add_param('rankingCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class RedisRowSinkStreamOp(BaseSinkStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sink.RedisRowSinkStreamOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RedisRowSinkStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setClusterMode(self, val):
        return self._add_param('clusterMode', val)

    def setDatabaseIndex(self, val):
        return self._add_param('databaseIndex', val)

    def setKeyCols(self, val):
        return self._add_param('keyCols', val)

    def setPipelineSize(self, val):
        return self._add_param('pipelineSize', val)

    def setRedisIPs(self, val):
        return self._add_param('redisIPs', val)

    def setRedisPassword(self, val):
        return self._add_param('redisPassword', val)

    def setTimeout(self, val):
        return self._add_param('timeout', val)

    def setValueCols(self, val):
        return self._add_param('valueCols', val)



class RedisStringSinkStreamOp(BaseSinkStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sink.RedisStringSinkStreamOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RedisStringSinkStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setClusterMode(self, val):
        return self._add_param('clusterMode', val)

    def setDatabaseIndex(self, val):
        return self._add_param('databaseIndex', val)

    def setKeyCol(self, val):
        return self._add_param('keyCol', val)

    def setPipelineSize(self, val):
        return self._add_param('pipelineSize', val)

    def setRedisIPs(self, val):
        return self._add_param('redisIPs', val)

    def setRedisPassword(self, val):
        return self._add_param('redisPassword', val)

    def setTimeout(self, val):
        return self._add_param('timeout', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)



class RegexTokenizerStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.nlp.RegexTokenizerStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RegexTokenizerStreamOp, self).__init__(*args, **kwargs)
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



class RidgeRegPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.regression.RidgeRegPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RidgeRegPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class SampleStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.SampleStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SampleStreamOp, self).__init__(*args, **kwargs)
        pass

    def setRatio(self, val):
        return self._add_param('ratio', val)

    def setWithReplacement(self, val):
        return self._add_param('withReplacement', val)



class SegmentStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.nlp.SegmentStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SegmentStreamOp, self).__init__(*args, **kwargs)
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



class SelectStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sql.SelectStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SelectStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)



class SessionTimeWindowStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.SessionTimeWindowStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SessionTimeWindowStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

    def setSessionGapTime(self, val):
        return self._add_param('sessionGapTime', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setLatency(self, val):
        return self._add_param('latency', val)

    def setWatermarkType(self, val):
        return self._add_param('watermarkType', val)



class ShiftStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.timeseries.ShiftStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ShiftStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictNum(self, val):
        return self._add_param('predictNum', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setShiftNum(self, val):
        return self._add_param('shiftNum', val)



class SideOutputStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.utils.SideOutputStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SideOutputStreamOp, self).__init__(*args, **kwargs)
        pass

    def setIndex(self, val):
        return self._add_param('index', val)



class SocketSinkStreamOp(BaseSinkStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sink.SocketSinkStreamOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SocketSinkStreamOp, self).__init__(*args, **kwargs)
        pass

    def setHost(self, val):
        return self._add_param('host', val)

    def setPort(self, val):
        return self._add_param('port', val)



class SoftmaxPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.classification.SoftmaxPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SoftmaxPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class SosOutlierStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.outlier.SosOutlierStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SosOutlierStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPrecedingTime(self, val):
        return self._add_param('precedingTime', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setPerplexity(self, val):
        return self._add_param('perplexity', val)

    def setPrecedingRows(self, val):
        return self._add_param('precedingRows', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class SplitStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.SplitStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SplitStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFraction(self, val):
        return self._add_param('fraction', val)

    def setRandomSeed(self, val):
        return self._add_param('randomSeed', val)



class StandardScalerPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.StandardScalerPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StandardScalerPredictStreamOp, self).__init__(*args, **kwargs)
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



class StopWordsRemoverStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.nlp.StopWordsRemoverStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StopWordsRemoverStreamOp, self).__init__(*args, **kwargs)
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



class StratifiedSampleStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.StratifiedSampleStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StratifiedSampleStreamOp, self).__init__(*args, **kwargs)
        pass

    def setStrataCol(self, val):
        return self._add_param('strataCol', val)

    def setStrataRatios(self, val):
        return self._add_param('strataRatios', val)

    def setStrataRatio(self, val):
        return self._add_param('strataRatio', val)



class StreamingKMeansStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.clustering.StreamingKMeansStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StreamingKMeansStreamOp, self).__init__(*args, **kwargs)
        pass

    def setHalfLife(self, val):
        return self._add_param('halfLife', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setTimeInterval(self, val):
        return self._add_param('timeInterval', val)

    def setPredictionClusterCol(self, val):
        return self._add_param('predictionClusterCol', val)

    def setPredictionDistanceCol(self, val):
        return self._add_param('predictionDistanceCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class StringIndexerPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.StringIndexerPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StringIndexerPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class StringSimilarityPairwiseStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.similarity.StringSimilarityPairwiseStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StringSimilarityPairwiseStreamOp, self).__init__(*args, **kwargs)
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



class SwingRecommStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.recommendation.SwingRecommStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SwingRecommStreamOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

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



class TFRecordDatasetSinkStreamOp(BaseSinkStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sink.TFRecordDatasetSinkStreamOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TFRecordDatasetSinkStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setNumFiles(self, val):
        return self._add_param('numFiles', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)



class TFRecordDatasetSourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.TFRecordDatasetSourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TFRecordDatasetSourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)



class TFSavedModelPredictStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.tensorflow.TFSavedModelPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TFSavedModelPredictStreamOp, self).__init__(*args, **kwargs)
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



class TFTableModelPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.tensorflow.TFTableModelPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TFTableModelPredictStreamOp, self).__init__(*args, **kwargs)
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

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setSignatureDefKey(self, val):
        return self._add_param('signatureDefKey', val)



class TensorFlow2StreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.tensorflow.TensorFlow2StreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TensorFlow2StreamOp, self).__init__(*args, **kwargs)
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

