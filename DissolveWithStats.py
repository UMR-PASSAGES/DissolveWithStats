# script parameters
##Dissolve with Stats=name
##Vector=group
##Input_layer=vector
##Dissolve_field=field Input_layer
##Statistics=string
##Output_layer=output vector

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField,
                       QgsProcessingParameterString
                       )
from qgis import processing


#from processing.core.parameters import Parameter
#from PyQt4 import QtCore
#from qgis.core import *
#from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
#from processing.tools.vector import VectorWriter
import os.path
#import processing
import sys
import time
import math

class DissolveWithStats(QgsProcessingAlgorithm):
    
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    DISSOLVE_FIELD = 'DISSOLVE_FIELD'
    STATISTICS = 'STATISTICS'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DissolveWithStats()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'dissolvewithstats'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Dissolve With Stats')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Example scripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'examplescripts'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Dissolve with one field and calculate statistics on other fields")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input vector layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        
        # adding parameter for dissolve field
        self.addParameter(
            QgsProcessingParameterField(
                self.DISSOLVE_FIELD,
                self.tr('Dissolve field'),
                None,
                self.INPUT
            )
        )
        
        # adding parameter for statistics
        self.addParameter(
            QgsProcessingParameterString(
                self.STATISTICS,
                self.tr('Statistics')
            )
        )

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )
        
    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(
            parameters,
            self.INPUT,
            context
        )

        # If source was not found, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSourceError method to return a standard
        # helper text for when a source cannot be evaluated
        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            source.fields(),
            source.wkbType(),
            source.sourceCrs()
        )
        
        Dissolve_field = self.parameterAsSource(
            parameters,
            self.DISSOLVE_FIELD,
            context
        )
        
        Statistics = self.parameterAsSource(
            parameters,
            self.STATISTICS,
            context
        )

        # run dissolve processing algorithm
        dissolve = processing.run("native:dissolve",
            {'INPUT' : parameters['INPUT'], 
            'FIELD' : parameters['DISSOLVE_FIELD'],
            'OUTPUT' : parameters['OUTPUT']})
        # get output of dissolve algorithm
        dissolveLayer = dissolve['OUTPUT']
        dissolveLayer = processing.getObject(dissolveLayer)
        # get list of statistics to compute for each field
        listStats = Statistics.split(';')
        # get object for input layer
        inputLayer = processing.getObject(source)

        def validation():
            # verifies that number of statistics = number of fields in input layer
            nbStats = len(listStats)
            provider = inputLayer.dataProvider()
            fields = provider.fields()
            nbFields = len(fields)
            if nbStats != nbFields:
                raise GeoAlgorithmExecutionException('Number of statistics is not equal to number of fields in input layer ; please check again.')

        # once the dissolve output layer is created, calculates its new attributes values
        def calculateFields(listStats, output):
            # iterates over input layer features to get attributes as a list of lists
            # uses the processing method so as to get only selected features if this option is set in the processing options
            iter = processing.features(inputLayer)
            attrs = [feature.attributes() for feature in iter]
            # get index of dissolve field
            provider = inputLayer.dataProvider()
            fields = provider.fields()
            listFieldNames = [field.name() for field in fields]
            indexDissolveField = listFieldNames.index(Dissolve_field)
            # get all values of the dissolve field (before processing : with duplicate values)
            valuesDissolveField = [feature[indexDissolveField] for feature in attrs]
            # get unique values for dissolve field, from output (seems more secure than to get it from valuesDissolveField ?)
            outputLayer = QgsVectorLayer(output, "name", "ogr")
            provider = dissolveLayer.dataProvider()
            fields = provider.fields()
            listFieldNames = [field.name() for field in fields]
            iter = outputLayer.getFeatures()
            uniqueValuesDissolveField = [feature.attributes()[indexDissolveField] for feature in iter]
            # initializes list of lists which will contain results (it will have one element per kept field)
            listRes = []
            # for each kept field
            for i in range(len(listFieldNames)):
                if listStats[i]  != 'no':
                    # creates list which will contain attribute values for current field, one empty element per unique dissolve field value
                    listAttrs = [[] for val in range(len(uniqueValuesDissolveField))]
                    # fill this list with all the current field values corresponding to each dissolve field value
                    valuesField = [feature[i] for feature in attrs]
                    for (x,y) in zip(valuesDissolveField, valuesField):
                        listAttrs[uniqueValuesDissolveField.index(x)].append(y)
                    # removes any NULL values
                    listAttrs = [[x for x in l if x] for l in listAttrs]
                    # for each list in listAttrs, calculates one value according to the chosen stat
                    # if list is empty (can happen if it contained originally only NULL values), return NULL as a result
                    if listStats[i] == "mean":
                        listAttrs = [sum(y) / len(y) if y else NULL for y in listAttrs]
                    elif listStats[i] == "sum":
                        listAttrs = [sum(y) if y else NULL for y in listAttrs]
                    elif listStats[i] == "min":
                        listAttrs = [min(y) if y else NULL for y in listAttrs]
                    elif listStats[i] == "max":
                        listAttrs = [max(y) if y else NULL for y in listAttrs]
                    elif listStats[i] == "count":
                        listAttrs = [len(y) if y else NULL for y in listAttrs]
                    elif listStats[i] == "first":
                        listAttrs = [y[0] if y else NULL for y in listAttrs]
                    elif listStats[i] == "last":
                        listAttrs = [y[-1] if y else NULL for y in listAttrs]
                    elif listStats[i] == "median":
                        listAttrs = [self.median(y) if y else NULL for y in listAttrs]
                    elif listStats[i] == "sd":
                        listAttrs = [self.standard_dev(y) if y else NULL for y in listAttrs]
                    elif listStats[i] == "concat":
                        listAttrs = [", ".join(y) if y else NULL for y in listAttrs]
                    elif listStats[i] == "unique":
                        listAttrs = [", ".join(set(y)) if y else NULL for y in listAttrs]
                    # append each field result to listRes
                    listRes.append(listAttrs)
            return listRes

        # removes fields from the output which mustn't be kept, and set the other field values            
        def setAttributes(listRes, output):
            # get indexes of fields to be deleted
            listIndexesDel = [i[0] for i in list(enumerate(listStats)) if i[1] == 'no']
            # get layer, provider and provider capabilities
            outputLayer = QgsVectorLayer(output, "name", "ogr")
            provider = outputLayer.dataProvider()
            caps = provider.capabilities()
            # delete fields to be deleted
            if caps & QgsVectorDataProvider.DeleteAttributes:
                res = provider.deleteAttributes(listIndexesDel)
                outputLayer.updateFields()
            # changes other fields attribute values
            fields = provider.fields()
            nb_fields = len(fields)
            outputLayer.startEditing()
            for fieldIndex in  range(nb_fields):
                for fid in range(len(listRes[0])):
                    outputLayer.changeAttributeValue(fid, fieldIndex, listRes[fieldIndex][fid])
            outputLayer.commitChanges()

        # gets the median from a list of numbers
        def median(self, l):
            # sorts list, get list length
            l.sort()
            z = len(l)
            # if the list has an uneven number of elements
            if z%2:
                return l[z/2]
            # if the list has an even number of elements
            else:
                return (l[(z/2)-1] + l[z/2]) / 2.0
                    
        # gets standard deviation from a list of numbers
        def standard_dev(self, l):
            mean = sum(l) / len(l)
            dev = [(x - mean)*(x - mean) for x in l]
            return math.sqrt(sum(dev) / len(l))

        validation()
        listRes = calculateFields(listStats, sink)
        setAttributes(listRes, sink)
    

