import logging
import os
from typing import Annotated, Optional

import vtk

import slicer
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.parameterNodeWrapper import (
    parameterNodeWrapper,
    WithinRange,
)

from slicer import vtkMRMLScalarVolumeNode

import numpy as np

import qt
#
# plateRegistration
#


class plateRegistration(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("plateRegistration")  # TODO: make this more human readable by adding spaces
        # TODO: set categories (folders where the module shows up in the module selector)
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Examples")]
        self.parent.dependencies = []  # TODO: add here list of module names that this module requires
        self.parent.contributors = ["Chi Zhang (Texas A&M University School of Dentistry)"]  # TODO: replace with "Firstname Lastname (Organization)"
        # TODO: update with short description of the module and a link to online module documentation
        # _() function marks text as translatable to other languages
        self.parent.helpText = _("""
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#plateRegistration">module documentation</a>.
""")
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = _("""
Will update soon
""")

        # Additional initialization step after application startup is complete
        # slicer.app.connect("startupCompleted()", registerSampleData)


#
# Register sample data sets in Sample Data module
#


# def registerSampleData():
#     """Add data sets to Sample Data module."""
#     # It is always recommended to provide sample data for users to make it easy to try the module,
#     # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.
# 
#     import SampleData
# 
#     iconsPath = os.path.join(os.path.dirname(__file__), "Resources/Icons")
# 
#     # To ensure that the source code repository remains small (can be downloaded and installed quickly)
#     # it is recommended to store data sets that are larger than a few MB in a Github release.
# 
#     # plateRegistration1
#     SampleData.SampleDataLogic.registerCustomSampleDataSource(
#         # Category and sample name displayed in Sample Data module
#         category="plateRegistration",
#         sampleName="plateRegistration1",
#         # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
#         # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
#         thumbnailFileName=os.path.join(iconsPath, "plateRegistration1.png"),
#         # Download URL and target file name
#         uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
#         fileNames="plateRegistration1.nrrd",
#         # Checksum to ensure file integrity. Can be computed by this command:
#         #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
#         checksums="SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
#         # This node name will be used when the data set is loaded
#         nodeNames="plateRegistration1",
#     )
# 
#     # plateRegistration2
#     SampleData.SampleDataLogic.registerCustomSampleDataSource(
#         # Category and sample name displayed in Sample Data module
#         category="plateRegistration",
#         sampleName="plateRegistration2",
#         thumbnailFileName=os.path.join(iconsPath, "plateRegistration2.png"),
#         # Download URL and target file name
#         uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
#         fileNames="plateRegistration2.nrrd",
#         checksums="SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
#         # This node name will be used when the data set is loaded
#         nodeNames="plateRegistration2",
#     )


#
# plateRegistrationParameterNode
#


# @parameterNodeWrapper
# class plateRegistrationParameterNode:
#     """
#     The parameters needed by module.
# 
#     inputVolume - The volume to threshold.
#     imageThreshold - The value at which to threshold the input volume.
#     invertThreshold - If true, will invert the threshold.
#     thresholdedVolume - The output volume that will contain the thresholded volume.
#     invertedVolume - The output volume that will contain the inverted thresholded volume.
#     """
# 
#     inputVolume: vtkMRMLScalarVolumeNode
#     imageThreshold: Annotated[float, WithinRange(-100, 500)] = 100
#     invertThreshold: bool = False
#     thresholdedVolume: vtkMRMLScalarVolumeNode
#     invertedVolume: vtkMRMLScalarVolumeNode
# 
# 
# #
# # plateRegistrationWidget
#


class plateRegistrationWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        self.logic = None
        self._parameterNode = None
        self._parameterNodeGuiTag = None

    def setup(self) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/plateRegistration.ui"))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = plateRegistrationLogic()

        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)
        
        #Input connections
        self.ui.inputOrbitVolSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
        self.ui.inputOrbitVolSelector.setMRMLScene(slicer.mrmlScene)
        # self.ui.inputOrbitModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
        # self.ui.inputOrbitModelSelector.setMRMLScene(slicer.mrmlScene)
        self.ui.inputOrbitModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
        self.ui.inputOrbitModelSelector.setMRMLScene(slicer.mrmlScene)
        self.ui.plateModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
        self.ui.plateModelSelector.setMRMLScene(slicer.mrmlScene)
        self.ui.plateFiducialSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
        self.ui.plateFiducialSelector.setMRMLScene(slicer.mrmlScene)
        
        #Initial registration connections
        self.ui.initialRegistrationPushButton.connect('clicked(bool)', self.onInitialRegistrationPushButton)
        self.ui.posteriorStopRegistrationPushButton.connect('clicked(bool)', self.onRotation_p_stop_pushButton)
        
        #Intersection model
        self.ui.createIntersectButton.connect('clicked(bool)', self.onCreateIntersectButton)
        # self.ui.createOverlappingModelButton.connect('clicked(bool)', self.onPaintModelwithOverlapButton)
        
        #interaction transform
        # self.ui.plateModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
        # self.ui.plateModelSelector.setMRMLScene(slicer.mrmlScene)
        # self.ui.inputOrbitModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
        # self.ui.inputOrbitModelSelector.setMRMLScene(slicer.mrmlScene)
        self.ui.orbitFiducialSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
        self.ui.orbitFiducialSelector.setMRMLScene(slicer.mrmlScene)
        #
        self.ui.interactionTransformCheckbox.connect("toggled(bool)", self.onInteractionTransform)
        #
        self.ui.realignHandleToPStopButton.connect('clicked(bool)', self.onRealignHandleToPStopButton)
        
        self.ui.resetToLastStepButton.connect('clicked(bool)', self.onResetToLastStepButton)
        
        # self.ui.computeNewOverlappingButton.connect('clicked(bool)', self.onComputeNewOverlappingButton)
        
        self.ui.resetAllButton.connect('clicked(bool)', self.onResetAllButton)

        # # Buttons
        # self.ui.applyButton.connect("clicked(bool)", self.onApplyButton)

        # # Make sure parameter node is initialized (needed for module reload)
        # self.initializeParameterNode()
        
        self.timer = qt.QTimer()
        self.timer.setInterval(500) #ms
        self.timer.setSingleShot(True)
        self.timer.connect("timeout()", self.timeout)

    def cleanup(self) -> None:
        """Called when the application closes and the module widget is destroyed."""
        self.removeObservers()

    def enter(self) -> None:
        """Called each time the user opens this module."""
        # Make sure parameter node exists and observed
        # self.initializeParameterNode()

    def exit(self) -> None:
        """Called each time the user opens a different module."""
        # Do not react to parameter node changes (GUI will be updated when the user enters into the module)
        # if self._parameterNode:
        #     self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
        #     self._parameterNodeGuiTag = None
        #     self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)

    def onSceneStartClose(self, caller, event) -> None:
        """Called just before the scene is closed."""
        # Parameter node will be reset, do not use it anymore
        # self.setParameterNode(None)

    def onSceneEndClose(self, caller, event) -> None:
        """Called just after the scene is closed."""
        # If this module is shown while the scene is closed then recreate a new parameter node immediately
        # if self.parent.isEntered:
        #     self.initializeParameterNode()
    
    def onSelect(self):
        #Enable initialRegistration push button
        self.ui.initialRegistrationPushButton.enabled = bool(self.ui.inputOrbitVolSelector.currentNode() and self.ui.inputOrbitModelSelector.currentNode() and self.ui.inputOrbitModelSelector.currentNode()
            and self.ui.plateModelSelector.currentNode() and self.ui.plateFiducialSelector.currentNode())
        #Enable posteriorStopRegistrationPushButton button
        # self.ui.posteriorStopRegistrationPushButton.enabled = bool(self.ui.initialRegistrationPushButton.enabled)
        # self.ui.interactionTransformCheckbox.enabled = bool(self.ui.plateModelSelector_2.currentNode() and self.ui.inputOrbitModelSelector_2.currentNode()
        #     and self.ui.orbitFiducialSelector_2.currentNode())

    
    def onInitialRegistrationPushButton(self):
        logic = plateRegistrationLogic()
        self.source_lm_node = self.ui.plateFiducialSelector.currentNode()
        self.target_lm_node = self.ui.orbitFiducialSelector.currentNode()
        initial_transform = logic.rigid_transform(self.source_lm_node, self.target_lm_node)
        initialTransformNode =  slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode', "initial_transform")
        initialTransformNode.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(initial_transform))
        #
        self.source_lm_node.SetAndObserveTransformNodeID(initialTransformNode.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.source_lm_node)
        self.source_model_node = self.ui.plateModelSelector.currentNode()
        self.source_model_node.SetAndObserveTransformNodeID(initialTransformNode.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.source_model_node)
        #Enable posteriorStopRegistrationPushButton button
        self.ui.posteriorStopRegistrationPushButton.enabled = True
        

    def onRotation_p_stop_pushButton(self):
        logic = plateRegistrationLogic()
        # source_lm_node = self.ui.plateFiducialSelector.currentNode()
        # target_lm_node = self.ui.inputOrbitModelSelector.currentNode()
        align_p_stop_transform = logic.align_p_stop(self.source_lm_node, self.target_lm_node)
        print(align_p_stop_transform)
        alignPStopTransformNode =  slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode', "align_p_stop_transform")
        alignPStopTransformNode.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(align_p_stop_transform))

        self.source_lm_node.SetAndObserveTransformNodeID(alignPStopTransformNode.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.source_lm_node)
        self.source_model_node.SetAndObserveTransformNodeID(alignPStopTransformNode.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.source_model_node)        

        p_stop_rotation = logic.rotation_p_stop(self.source_lm_node, self.target_lm_node)
        print(p_stop_rotation)
        p_stop_rotation_node =  slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode', "p_stop_rotation")
        p_stop_rotation_node.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(p_stop_rotation))
        #
        self.source_lm_node.SetAndObserveTransformNodeID(p_stop_rotation_node.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.source_lm_node)
        # source_model_node = self.ui.plateModelSelector.currentNode()
        self.source_model_node.SetAndObserveTransformNodeID(p_stop_rotation_node.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.source_model_node)
        #
        self.ui.interactionTransformCheckbox.enabled = True
        # self.ui.createIntersectButton.enabled = True
        
        
        
    def onCreateIntersectButton(self):
        logic = plateRegistrationLogic()
        try:
            slicer.mrmlScene.RemoveNode(self.intersectionModel)
        except:
            pass
        #clone plate remesh
        shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
        itemIDToClone = shNode.GetItemByDataNode(self.plateRemeshNode)
        clonedItemID = slicer.modules.subjecthierarchy.logic().CloneSubjectHierarchyItem(shNode, itemIDToClone)
        self.plateRemeshNode_clone = shNode.GetItemDataNode(clonedItemID)
        
        #Add to interaction trasnform and harden it
        self.plateRemeshNode_clone.SetAndObserveTransformNodeID(self.interactionTransformNode.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.plateRemeshNode_clone)
        #
        collisionFlag, numberOfCollisions = logic.collision_detection(self.plateRemeshNode_clone, self.orbitModelCropped)
        #output information
        self.ui.collisionInfoBox.clear
        if collisionFlag == True:
            self.ui.collisionInfoBox.insertPlainText(
              f":: Collision between model and plate detected. There are {numberOfCollisions} collision points. \n"
            )
            intersector = logic.intersection_marker(self.plateRemeshNode_clone, self.orbitModelCropped)
            self.intersectionModel = slicer.modules.models.logic().AddModel(intersector.GetOutputDataObject(0))
            self.intersectionModel.SetName("intersectionModel_0")
            yellow = [255, 255, 0]
            self.intersectionModel.GetDisplayNode().SetColor(yellow)
            self.intersectionModel.GetDisplayNode().SetVisibility2D(True)
            self.intersectionModel.GetDisplayNode().SetSliceIntersectionThickness(7)
        else:
            self.ui.collisionInfoBox.insertPlainText(
              f":: No collision detected. \n"
            )
        # self.ui.createOverlappingModelButton.enabled = True
        #Remove nodes
        slicer.mrmlScene.RemoveNode(self.plateRemeshNode_clone)
    
    
    # def onPaintModelwithOverlapButton(self):
    #     logic = plateRegistrationLogic()
    #     #Create segments from plate and orbit models
    #     segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
    #     segmentationNode.CreateDefaultDisplayNodes()
    #     # segmentationNode.Set
    #     slicer.modules.segmentations.logic().ImportModelToSegmentationNode(self.source_model_node, segmentationNode)
    #     slicer.modules.segmentations.logic().ImportModelToSegmentationNode(self.orbit_model_node, segmentationNode)
    #     
    #     #Get master volume 
    #     masterVolumeNode = self.ui.inputOrbitVolSelector.currentNode()
    #     
    #     #Create segment editor to get access to effects
    #     segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
    #     segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
    #     segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
    #     segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
    #     segmentEditorWidget.setSegmentationNode(segmentationNode)        
    # 
    #     #Logic operator: intersect
    #     segmentEditorWidget.setActiveEffectByName("Logical operators")
    #     effect = segmentEditorWidget.activeEffect()
    #     effect.setParameter("Operation","INTERSECT")
    #     #get segments
    #     plateSegID = segmentationNode.GetSegmentation().GetSegmentIDs()[0]
    #     boneSegID = segmentationNode.GetSegmentation().GetSegmentIDs()[1]
    #     plateSeg = segmentationNode.GetSegmentation().GetSegment(plateSegID)
    #     boneSeg = segmentationNode.GetSegmentation().GetSegment(boneSegID)
    #     #
    #     segmentEditorNode.SetSelectedSegmentID(plateSegID)
    #     effect.setParameter("ModifierSegmentID", boneSegID)
    #     effect.self().onApply()
    #     
    #     #Grow margin
    #     segmentEditorWidget.setActiveEffectByName("Margin")
    #     effect = segmentEditorWidget.activeEffect()
    #     effect.setParameter("MarginSizeMm", 0.25)
    #     segmentEditorNode.SetSelectedSegmentID(plateSegID)
    #     effect.self().onApply()
    # 
    #     #Remove bone segment
    #     segmentationNode.GetSegmentation().RemoveSegment(boneSegID)
    #     #
    #     plate_painted_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode")
    #     logic.paint_model_by_volume(segmentationNode, masterVolumeNode, self.source_model_node, plate_painted_node)
    #     plate_painted_node.SetName('plate_intersect_marked')
    #     orbit_painted_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode")
    #     logic.paint_model_by_volume(segmentationNode, masterVolumeNode, self.orbit_model_node, orbit_painted_node)
    #     orbit_painted_node.SetName('orbit_intersect_marked')
    #     #
    #     
    #     plate_painted_node.GetDisplayNode().SetVisibility2D(True)
    #     plate_painted_node.GetDisplayNode().SetSliceIntersectionThickness(2)        
    # 
    # 
    #     #Shrink margin
    #     segmentEditorWidget.setActiveEffectByName("Margin")
    #     effect = segmentEditorWidget.activeEffect()
    #     effect.setParameter("MarginSizeMm", -0.25)
    #     segmentEditorNode.SetSelectedSegmentID(plateSegID)
    #     effect.self().onApply()
    # 
    #     #Segment statistics
    #     import SegmentStatistics
    #     segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
    #     segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
    #     segStatLogic.computeStatistics()
    #     stats = segStatLogic.getStatistics()
    # 
    #     # Display volume of each segment
    #     # for segmentId in stats["SegmentIDs"]:
    #     #   volume_cm3 = stats[segmentId,"LabelmapSegmentStatisticsPlugin.volume_cm3"]
    #     #   segmentName = segmentationNode.GetSegmentation().GetSegment(segmentId).GetName()
    #     #   self.ui.collisionInfoBox.insertPlainText(
    #     #     f":: the overlapping volume between the plate and the orbit is {volume_cm3} cm3. \n"
    #     #   )
    #     volume_mm3 = stats[plateSegID,"LabelmapSegmentStatisticsPlugin.volume_mm3"]
    #     print(stats)
    #     print(volume_mm3)
    #     self.ui.collisionInfoBox.insertPlainText(
    #       f":: the overlapping volume between the plate and the orbit is {volume_mm3} mm3. \n"
    #     )
    # 
    #     segDisplayNode = segmentationNode.GetDisplayNode()
    #     segDisplayNode.SetSegmentVisibility(plateSegID, False)
        
        
    def onInteractionTransform(self):
        if self.ui.interactionTransformCheckbox.isChecked():
            # self.ui.computeNewOverlappingButton.enabled = False
            self.interactionTransformNode =  slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode', "interaction_transform")
            self.plateModelNode2 = self.ui.plateModelSelector.currentNode()
            # self.plateModelNode2.SetAndObserveTransformNodeID(self.interactionTransformNode.GetID())
            self.interactionTransformNode.CreateDefaultDisplayNodes()
            # self.interactionTransformNode.GetDisplayNode().SetActiveInteractionType()
            # self.interactionTransformNode.SetDisplayVisibility(True)
            # self.interactionTransformNode.GetDisplayNode().SetVisibility(True)
            self.interactionTransformNode.GetDisplayNode().SetEditorVisibility(True) #visualize in 3D and 2D
            #Set center to posterior stop
            self.newOrbitLmNode = self.ui.orbitFiducialSelector.currentNode()
            self.interactionTransformNode.SetCenterOfTransformation(self.newOrbitLmNode.GetNthControlPointPosition(1))
            #Add plate to the intraction transfrom
            # self.newPlateModelNode = self.ui.plateModelSelector_2.currentNode()
            # self.newPlateModelNode.SetAndObserveTransformNodeID(self.interactionTransformNode.GetID())
            # if self.fullTransformNode in locals():
            if slicer.mrmlScene.GetFirstNodeByName('fullTransform'):
                self.fullTransformNode = slicer.mrmlScene.GetFirstNodeByName('fullTransform')
                self.fullTransformNode.SetAndObserveTransformNodeID(self.interactionTransformNode.GetID())
            else:
                self.fullTransformNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode', "fullTransform")
                # self.fullTransformNode.GetDisplayNode().SetActiveInteractionType()
                # self.fullTransformNode.GetDisplayNode().SetVisibility(False)
                # self.fullTransformNode.GetDisplayNode().SetEditorVisibility(False)
                #Put fullTransformNode under interactionTransformNode = np.dot(interactionTransformNode, fullTransformNode)
                self.fullTransformNode.SetAndObserveTransformNodeID(self.interactionTransformNode.GetID())
            self.ui.realignHandleToPStopButton.enabled = True
            self.ui.resetToLastStepButton.enabled = True
            self.ui.createIntersectButton.enabled = True
            self.ui.resetAllButton.enabled = True
    
            #remesh plate model to 10k points
            import SurfaceToolbox
            surfaceToolboxLogic = SurfaceToolbox.SurfaceToolboxLogic()
            self.plateRemeshNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode")
            self.plateRemeshNode.SetName("plate_remesh")
            self.plateRemeshNode.CreateDefaultDisplayNodes()
            self.plateRemeshNode.AddDefaultStorageNode()
            surfaceToolboxLogic.remesh(inputModel = self.source_model_node, outputModel=self.plateRemeshNode, subdivide=0, clusters=10000)
            self.source_model_node.GetDisplayNode().SetVisibility(False)
            self.plateRemeshNode.GetDisplayNode().SetVisibility(True)
            self.plateRemeshNode.GetDisplayNode().SetVisibility2D(True)
            self.plateRemeshNode.GetDisplayNode().SetSliceIntersectionThickness(3)
            self.plateRemeshNode.SetAndObserveTransformNodeID(self.interactionTransformNode.GetID())
    
            #Connect to the timer
            try:
                self.interactionTransformNode.RemoveObserver(observerTag1)
            except:
                pass
            observerTag1 = self.interactionTransformNode.AddObserver(slicer.vtkMRMLTransformNode.TransformModifiedEvent, self.executeTimer)

    def timerFunction(self):
        self.timer.start()

    def executeTimer(self, caller, eventid):
        # print("found event")
        self.timerFunction()
        # print("event found2")
        #When modifier the transform, update timer

    def timeout(self):
        logic = plateRegistrationLogic()
        print("timeout")
        #Turn remeshed plate to labelmap and create an ROI fit to it
        segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
        segmentationNode.CreateDefaultDisplayNodes()
        segmentationNode.SetName('segmentation_plate_down')
        slicer.modules.segmentations.logic().ImportModelToSegmentationNode(self.plateRemeshNode, segmentationNode)
        segmentationNode.CreateBinaryLabelmapRepresentation()
        outputLabelmapVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLabelMapVolumeNode")
        slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(segmentationNode, outputLabelmapVolumeNode)
        roiNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsROINode")
        roiNode.CreateDefaultDisplayNodes()
        cropVolumeParameters = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLCropVolumeParametersNode")
        cropVolumeParameters.SetInputVolumeNodeID(outputLabelmapVolumeNode.GetID())
        cropVolumeParameters.SetROINodeID(roiNode.GetID())
        slicer.modules.cropvolume.logic().SnapROIToVoxelGrid(cropVolumeParameters)  # optional (rotates the ROI to match the volume axis directions)
        slicer.modules.cropvolume.logic().FitROIToInputVolume(cropVolumeParameters)
        slicer.mrmlScene.RemoveNode(cropVolumeParameters)
        slicer.mrmlScene.RemoveNode(segmentationNode)
        slicer.mrmlScene.RemoveNode(outputLabelmapVolumeNode)
        #
        #Use ROI to crop the orbit model; dynamic modeler
        try:
            slicer.mrmlScene.RemoveNode(self.orbitModelCropped)
        except:
            pass
        roiCutTool = slicer.vtkSlicerDynamicModelerROICutTool()
        
        self.orbitModelCropped = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode")
        self.orbitModelCropped.SetName("orbit_cropped")
        self.orbitModelCropped.CreateDefaultDisplayNodes()
        self.plateRemeshNode.AddDefaultStorageNode()
        
        dynamicModelerNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLDynamicModelerNode")
        dynamicModelerNode.SetToolName("ROI cut")
        self.orbit_model_node = self.ui.inputOrbitModelSelector.currentNode()
        # self.orbit_model_node.GetDisplayNode().SetColor([255, 255, 255])
        self.orbit_model_node.GetDisplayNode().SetOpacity(0.6)
        dynamicModelerNode.SetNodeReferenceID("ROICut.InputModel", self.orbit_model_node.GetID())
        dynamicModelerNode.SetNodeReferenceID("ROICut.InputROI", roiNode.GetID())
        dynamicModelerNode.SetNodeReferenceID("ROICut.OutputPositiveModel", self.orbitModelCropped.GetID())
        slicer.modules.dynamicmodeler.logic().RunDynamicModelerTool(dynamicModelerNode)
        roiNode.GetDisplayNode().SetVisibility(False)
        slicer.mrmlScene.RemoveNode(dynamicModelerNode)
        slicer.mrmlScene.RemoveNode(roiNode)
        
        #remesh cropped orbit
        import SurfaceToolbox
        surfaceToolboxLogic = SurfaceToolbox.SurfaceToolboxLogic()
        # orbitModelCropped_remesh = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode")
        # orbitModelCropped_remesh.SetName("orbit_remesh")
        # orbitModelCropped_remesh.CreateDefaultDisplayNodes()
        # orbitModelCropped_remesh.AddDefaultStorageNode()
        surfaceToolboxLogic.remesh(inputModel = self.orbitModelCropped, outputModel=self.orbitModelCropped, subdivide=0, clusters=10000)
        self.orbitModelCropped.GetDisplayNode().SetVisibility(True)
        
        collisionFlag, numberOfCollisions = logic.collision_detection(plate_node = self.plateRemeshNode, orbit_node = self.orbitModelCropped)
        if collisionFlag == False:
            self.ui.collisionInfoBox.insertPlainText(
              f":: No collision detected. \n"
            )
        else:
            print( "{} Collisions Detected".format( numberOfCollisions ) )
            #If collision is detected, do a model to model distance and get a heatmap
            # plateMesh = slicer.util.getNode('ouputDistanceMap')
            #create plate heatmap
            slicer.vtkSlicerTransformLogic().hardenTransform(self.plateRemeshNode)
            plate_distanceMap, self.plateRemeshNode=logic.heatmap(templateMesh = self.plateRemeshNode, currentMesh = self.orbitModelCropped)
            d = self.plateRemeshNode.GetDisplayNode()
            d.SetScalarVisibility(True)
            d.SetActiveScalarName('Distance')
            d.SetAndObserveColorNodeID("RedGreenBlue")
            d.SetScalarRangeFlagFromString('Manual')
            d.SetScalarRange(-3, 0.5)
            # d.SetThresholdEnabled(True)
            # d.SetThresholdRange(-1, 1)
            #Add plate node to the interaction transform again in the end
            # transformMatrix = vtk.vtkMatrix4x4() #identiy matrix
            # self.interactionTransformNode.SetMatrixTransformToParent(transformMatrix)
            # self.plateRemeshNode.SetAndObserveTransformNodeID(self.interactionTransformNode.GetID())
            # slicer.mrmlScene.RemoveNode(self.interactionTransformNode)
            # self.onInteractionTransform()
            #create a new plate_remesh from original model and add to transform
            # #apply a distance map to it and remove the last one
            # import SurfaceToolbox
            # surfaceToolboxLogic = SurfaceToolbox.SurfaceToolboxLogic()
            # self.plateRemeshNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode")
            # self.plateRemeshNode.SetName("plate_remesh")
            # self.plateRemeshNode.CreateDefaultDisplayNodes()
            # self.plateRemeshNode.AddDefaultStorageNode()
            # surfaceToolboxLogic.remesh(inputModel = self.source_model_node, outputModel=self.plateRemeshNode, subdivide=0, clusters=10000)
            # self.source_model_node.GetDisplayNode().SetVisibility(False)
            # self.plateRemeshNode.GetDisplayNode().SetVisibility(True)
            #Clone current interaction transform and inverse it
            shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
            itemIDToClone = shNode.GetItemByDataNode(self.interactionTransformNode)
            clonedItemID = slicer.modules.subjecthierarchy.logic().CloneSubjectHierarchyItem(shNode, itemIDToClone)
            self.interactionTransform_inverse = shNode.GetItemDataNode(clonedItemID)
            self.interactionTransform_inverse.SetName('interactionTransform_inverse')
            self.interactionTransform_inverse.Inverse()
            #
            #Inverse transform the plateRemesh node and add back to interaction transform
            self.plateRemeshNode.SetAndObserveTransformNodeID(self.interactionTransform_inverse.GetID())
            slicer.vtkSlicerTransformLogic().hardenTransform(self.plateRemeshNode)
            self.plateRemeshNode.SetAndObserveTransformNodeID(self.interactionTransformNode.GetID())
            slicer.mrmlScene.RemoveNode(self.interactionTransform_inverse)
            #remove plateRemeshNode
            # slicer.mrmlScene.RemoveNode(self.plateRemeshNode)
            
            #create orbit heatmap
            orbit_distanceMap, self.orbitModelCropped=logic.heatmap(templateMesh = self.orbitModelCropped, currentMesh = self.plateRemeshNode)
            d = self.orbitModelCropped.GetDisplayNode()
            d.SetScalarVisibility(True)
            d.SetActiveScalarName('Distance')
            d.SetAndObserveColorNodeID("RedGreenBlue")
            d.SetScalarRangeFlagFromString('Manual')
            d.SetScalarRange(-2, 2)
            d.SetThresholdEnabled(True)
            d.SetThresholdRange(0, 2)


    def onRealignHandleToPStopButton(self):
        self.newOrbitLmNode = self.ui.orbitFiducialSelector.currentNode()
        # Clone orbit lm
        shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
        itemIDToClone = shNode.GetItemByDataNode(self.newOrbitLmNode)
        clonedItemID = slicer.modules.subjecthierarchy.logic().CloneSubjectHierarchyItem(shNode, itemIDToClone)
        self.orbitLmCloneNode = shNode.GetItemDataNode(clonedItemID)
        self.orbitLmCloneNode.SetName('orbit_lm_cloned')
        self.orbitLmCloneNode.SetAndObserveTransformNodeID(self.interactionTransformNode.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.orbitLmCloneNode)
        
        # self.interactionTransformNode.SetCenterOfTransformation(self.newOrbitLmNode.GetNthControlPointPosition(1))
        p_stop_source = [0, 0, 0]
        self.orbitLmCloneNode.GetNthControlPointPosition(1, p_stop_source)
        
        p_stop_target = [0, 0, 0 ]
        self.newOrbitLmNode.GetNthControlPointPosition(1, p_stop_target)
        
        translation = np.subtract(p_stop_target, p_stop_source)
        
        # homogeneous transformation
        realignPStopTransform = np.identity(4)
        realignPStopTransform[:3, 3] = translation
        
        realignPStopTransformNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode', "realignPStopTransform")
        realignPStopTransformNode.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(realignPStopTransform))

        self.interactionTransformNode.SetAndObserveTransformNodeID(realignPStopTransformNode.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.interactionTransformNode)
        
        slicer.mrmlScene.RemoveNode(realignPStopTransformNode)
        slicer.mrmlScene.RemoveNode(self.orbitLmCloneNode)

        


    def onResetToLastStepButton(self):
        transformMatrix = vtk.vtkMatrix4x4() #identiy matrix
        self.interactionTransformNode.SetMatrixTransformToParent(transformMatrix)
        #self.fullTransFormNode is also updated

    # def onComputeNewOverlappingButton(self):
    #     try: 
    #         intersectionNode_previous = slicer.util.getNode('intersectionModel_0')
    #         intersectionNode_previous.GetDisplayNode().SetVisibility(False)
    #     except MRMLNodeNotFoundException:
    #         pass
    #     logic = plateRegistrationLogic()
    #     # self.plateModelNode2 = self.ui.plateModelSelector_2.currentNode()
    #     slicer.vtkSlicerTransformLogic().hardenTransform(self.plateModelNode2)
    #     self.orbitModelNode2 = self.ui.inputOrbitModelSelector.currentNode()
    #     self.orbitLmNode2 = self.ui.orbitFiducialSelector.currentNode()
    #     collisionFlag, numberOfCollisions = logic.collision_detection(self.plateModelNode2, self.orbitModelNode2)
    #     #output information
    #     self.ui.collisionInfoBox2.clear
    #     if collisionFlag == True:
    #         self.ui.collisionInfoBox2.insertPlainText(
    #           f":: Collision between model and plate detected. There are {numberOfCollisions} collision points. \n"
    #         )
    #         intersector = logic.intersection_marker(self.plateModelNode2, self.orbitModelNode2)
    #         intersectionModel = slicer.modules.models.logic().AddModel(intersector.GetOutputDataObject(0))
    #         intersectionModel.SetName("intersectionModel_0")
    #         yellow = [255, 255, 0]
    #         intersectionModel.GetDisplayNode().SetColor(yellow)
    #         intersectionModel.GetDisplayNode().SetVisibility2D(True)
    #         intersectionModel.GetDisplayNode().SetSliceIntersectionThickness(7)
    #     else:
    #         self.ui.collisionInfoBox2.insertPlainText(
    #           f":: No collision detected. \n"
    #         )
    #     
    #     #Create segments from plate and orbit models
    #     segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
    #     segmentationNode.CreateDefaultDisplayNodes()
    #     segmentationNode.SetName('segmentation_2')
    #     slicer.modules.segmentations.logic().ImportModelToSegmentationNode(self.plateModelNode2, segmentationNode)
    #     slicer.modules.segmentations.logic().ImportModelToSegmentationNode(self.orbitModelNode2, segmentationNode)
    #     
    #     #Get master volume 
    #     masterVolumeNode = self.ui.inputOrbitVolSelector.currentNode()
    #     
    #     #Create segment editor to get access to effects
    #     segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
    #     segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
    #     segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
    #     segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
    #     segmentEditorWidget.setSegmentationNode(segmentationNode)        
    # 
    #     #Logic operator: intersect
    #     segmentEditorWidget.setActiveEffectByName("Logical operators")
    #     effect = segmentEditorWidget.activeEffect()
    #     effect.setParameter("Operation","INTERSECT")
    #     #get segments
    #     plateSegID = segmentationNode.GetSegmentation().GetSegmentIDs()[0]
    #     boneSegID = segmentationNode.GetSegmentation().GetSegmentIDs()[1]
    #     plateSeg = segmentationNode.GetSegmentation().GetSegment(plateSegID)
    #     boneSeg = segmentationNode.GetSegmentation().GetSegment(boneSegID)
    #     #
    #     segmentEditorNode.SetSelectedSegmentID(plateSegID)
    #     effect.setParameter("ModifierSegmentID", boneSegID)
    #     effect.self().onApply()
    # 
    #     #Grow margin
    #     segmentEditorWidget.setActiveEffectByName("Margin")
    #     effect = segmentEditorWidget.activeEffect()
    #     effect.setParameter("MarginSizeMm", 0.25)
    #     segmentEditorNode.SetSelectedSegmentID(plateSegID)
    #     effect.self().onApply()
    # 
    #     #Remove bone segment
    #     segmentationNode.GetSegmentation().RemoveSegment(boneSegID)
    #     #
    #     logic.paint_model_by_volume(segmentationNode, masterVolumeNode, self.plateModelNode2, self.plateModelNode2)
    #     # plate_painted2.SetName('plate_intersect_marked_interaction')
    #     logic.paint_model_by_volume(segmentationNode, masterVolumeNode, self.orbitModelNode2, self.orbitModelNode2)
    #     # orbit_painted2.SetName('orbit_intersect_marked_interaction')
    #     
    #     self.plateModelNode2.GetDisplayNode().SetVisibility2D(True)
    #     self.plateModelNode2.GetDisplayNode().SetSliceIntersectionThickness(2)
    #     
    #     # self.plateModelNode2.GetDisplayNode().SetAndObserveColorNodeID("Iron")
    #     # self.plateModelNode2.GetDisplayNode().SetScalarVisibility(True)
    # 
    #     #Shrink margin
    #     segmentEditorWidget.setActiveEffectByName("Margin")
    #     effect = segmentEditorWidget.activeEffect()
    #     effect.setParameter("MarginSizeMm", -0.25)
    #     segmentEditorNode.SetSelectedSegmentID(plateSegID)
    #     effect.self().onApply()
    # 
    #     #Segment statistics
    #     import SegmentStatistics
    #     segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
    #     segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
    #     segStatLogic.computeStatistics()
    #     stats = segStatLogic.getStatistics()
    # 
    #     volume_mm3 = stats[plateSegID,"LabelmapSegmentStatisticsPlugin.volume_mm3"]
    #     print(stats)
    #     print(volume_mm3)
    #     self.ui.collisionInfoBox2.insertPlainText(
    #       f":: the overlapping volume between the plate and the orbit is {volume_mm3} mm3. \n"
    #     )
    # 
    #     segDisplayNode = segmentationNode.GetDisplayNode()
    #     segDisplayNode.SetSegmentVisibility(plateSegID, False)
    # 
    #     self.ui.interactionTransformCheckbox.checked = 0
    #     self.ui.resetToLastStepButton.enabled = False
    #     # self.ui.computeNewOverlappingButton.enabled = False
    #     slicer.vtkSlicerTransformLogic().hardenTransform(self.fullTransformNode)
    #     #
    #     # self.interactionTransformNode.GetDisplayNode().SetEditorVisibility(False)
    #     slicer.mrmlScene.RemoveNode(self.interactionTransformNode)
    #     # self.ui.resetAllButton.enabled = True




    def onResetAllButton(self):
        # self.timer.stop()
        # self.ui.computeNewOverlappingButton.enabled = False
        slicer.vtkSlicerTransformLogic().hardenTransform(self.fullTransformNode)
        # slicer.vtkSlicerTransformLogic().hardenTransform(self.plateModelNode2)

        # Clone the fulltransform node for inverse
        # shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
        # itemIDToClone = shNode.GetItemByDataNode(self.fullTransformNode)
        # clonedItemID = slicer.modules.subjecthierarchy.logic().CloneSubjectHierarchyItem(shNode, itemIDToClone)
        # self.fullInverseTransformNode = shNode.GetItemDataNode(clonedItemID)
        # self.fullInverseTransformNode.SetName('fullInverseTransform')
        # self.fullInverseTransformNode.Inverse()
        # self.plateModelNode2.SetAndObserveTransformNodeID(self.fullInverseTransformNode.GetID())
        # slicer.vtkSlicerTransformLogic().hardenTransform(self.plateModelNode2)
        
        # Clone the fullTransformNode from the last step
        shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
        itemIDToClone = shNode.GetItemByDataNode(self.interactionTransformNode)
        clonedItemID = slicer.modules.subjecthierarchy.logic().CloneSubjectHierarchyItem(shNode, itemIDToClone)
        self.fullTransformNode_previous = shNode.GetItemDataNode(clonedItemID)
        self.fullTransformNode_previous.SetName('fullTransform_previous')
        
        slicer.mrmlScene.RemoveNode(self.fullTransformNode)
        slicer.mrmlScene.RemoveNode(self.plateRemeshNode)
        slicer.mrmlScene.RemoveNode(self.interactionTransformNode)
        slicer.mrmlScene.RemoveNode(self.orbitModelCropped)
        self.ui.realignHandleToPStopButton.enabled = False
        self.ui.resetAllButton.enabled = False
        self.ui.interactionTransformCheckbox.checked = 0
        self.ui.resetToLastStepButton.enabled = False
        self.source_model_node.GetDisplayNode().SetVisibility(True)
        
        # slicer.mrmlScene.RemoveNode()


    # def initializeParameterNode(self) -> None:
    #     """Ensure parameter node exists and observed."""
    #     # Parameter node stores all user choices in parameter values, node selections, etc.
    #     # so that when the scene is saved and reloaded, these settings are restored.
    # 
    #     self.setParameterNode(self.logic.getParameterNode())
    # 
    #     # Select default input nodes if nothing is selected yet to save a few clicks for the user
    #     if not self._parameterNode.inputVolume:
    #         firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
    #         if firstVolumeNode:
    #             self._parameterNode.inputVolume = firstVolumeNode

    # def setParameterNode(self, inputParameterNode: Optional[plateRegistrationParameterNode]) -> None:
    #     """
    #     Set and observe parameter node.
    #     Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
    #     """
    # 
    #     if self._parameterNode:
    #         self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
    #         self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
    #     self._parameterNode = inputParameterNode
    #     if self._parameterNode:
    #         # Note: in the .ui file, a Qt dynamic property called "SlicerParameterName" is set on each
    #         # ui element that needs connection.
    #         self._parameterNodeGuiTag = self._parameterNode.connectGui(self.ui)
    #         self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
    #         self._checkCanApply()

    # def _checkCanApply(self, caller=None, event=None) -> None:
    #     if self._parameterNode and self._parameterNode.inputVolume and self._parameterNode.thresholdedVolume:
    #         self.ui.applyButton.toolTip = _("Compute output volume")
    #         self.ui.applyButton.enabled = True
    #     else:
    #         self.ui.applyButton.toolTip = _("Select input and output volume nodes")
    #         self.ui.applyButton.enabled = False

    # def onApplyButton(self) -> None:
    #     """Run processing when user clicks "Apply" button."""
    #     with slicer.util.tryWithErrorDisplay(_("Failed to compute results."), waitCursor=True):
    #         # Compute output
    #         self.logic.process(self.ui.inputSelector.currentNode(), self.ui.outputSelector.currentNode(),
    #                            self.ui.imageThresholdSliderWidget.value, self.ui.invertOutputCheckBox.checked)
    # 
    #         # Compute inverted output (if needed)
    #         if self.ui.invertedOutputSelector.currentNode():
    #             # If additional output volume is selected then result with inverted threshold is written there
    #             self.logic.process(self.ui.inputSelector.currentNode(), self.ui.invertedOutputSelector.currentNode(),
    #                                self.ui.imageThresholdSliderWidget.value, not self.ui.invertOutputCheckBox.checked, showResult=False)


#
# plateRegistrationLogic
#


class plateRegistrationLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self) -> None:
        """Called when the logic class is instantiated. Can be used for initializing member variables."""
        ScriptedLoadableModuleLogic.__init__(self)

    def rigid_transform(self, source_lm_node, target_lm_node):
        source_points = np.zeros(shape=(source_lm_node.GetNumberOfControlPoints(), 3))
        target_points = np.zeros(shape=(target_lm_node.GetNumberOfControlPoints(), 3))
        
        m = source_points.shape[1]
        
        point = [0, 0, 0]
        
        for i in range(source_lm_node.GetNumberOfControlPoints()):
            source_lm_node.GetNthControlPointPosition(i, point)
            source_points[i, :] = point
            # subjectFiducial.SetNthControlPointLocked(i, 1)
            target_lm_node.GetNthControlPointPosition(i, point)
            target_points[i, :] = point

        
        points_number = source_points.shape[1]
        
        #translate points to centroids
        source_centroid = np.mean(source_points, axis = 0)
        target_centroid = np.mean(target_points, axis = 0)
        source_centered_points = source_points - source_centroid
        target_centered_points = target_points - target_centroid
        
        #transformation matrix
        # Perform singular value decomposition (SVD)
        U, _, Vt = np.linalg.svd(source_centered_points.T @ target_centered_points, full_matrices=False)
        
        # Calculate the optimal rotation matrix
        rotation_matrix = Vt.T @ U.T
        
        # special reflection case
        if np.linalg.det(rotation_matrix) < 0:
            Vt[m - 1, :] *= -1
        rotation_matrix = np.dot(Vt.T, U.T)
        
        #translation
        t = target_centroid.T - np.dot(rotation_matrix, source_centroid.T)
        
        # homogeneous transformation matrix
        T = np.identity(4)
        T[:3, :3] = rotation_matrix
        T[:3, 3] = t
        
        # rotationTransformNode =  slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode', "svd_rotation_transform")
        # rotationTransformNode.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(T))
        
        return T

    
    def align_p_stop(self, source_node, target_node):
        p_stop_source = [0, 0, 0]
        source_node.GetNthControlPointPosition(1, p_stop_source)
        
        p_stop_target = [0, 0, 0 ]
        target_node.GetNthControlPointPosition(1, p_stop_target)
        
        translation = np.subtract(p_stop_target, p_stop_source)
        
        # homogeneous transformation
        T = np.identity(4)
        T[:3, 3] = translation
        
        print(T)
        
        return T

    
    
    def rotation_p_stop(self, source_node, target_node):

        source_points = np.zeros(shape=(source_node.GetNumberOfControlPoints(), 3))
        target_points = np.zeros(shape=(target_node.GetNumberOfControlPoints(), 3))
        
        m = source_points.shape[1]
        
        point = [0, 0, 0]
        
        for i in range(source_node.GetNumberOfControlPoints()):
          source_node.GetNthControlPointPosition(i, point)
          source_points[i, :] = point
          # subjectFiducial.SetNthControlPointLocked(i, 1)
          target_node.GetNthControlPointPosition(i, point)
          target_points[i, :] = point
        
        # Define the point around which you want to rotate
        rotation_center = target_points[1, :] # Specify the center point as the posterior stop
        
        # Calculate the translation to bring the rotation center to the origin
        translation = -rotation_center
        
        # Translate both the source and target point sets
        translated_source_points = source_points + translation
        translated_target_points = target_points + translation
        
        # Perform singular value decomposition (SVD)
        U, _, Vt = np.linalg.svd(translated_source_points.T @ translated_target_points, full_matrices=False)
        
        
        # Calculate the optimal rotation matrix
        rotation_matrix = Vt.T @ U.T
        
        # special reflection case
        m = translated_source_points.shape[1]
        if np.linalg.det(rotation_matrix) < 0:
            Vt[m - 1, :] *= -1
        rotation_matrix = np.dot(Vt.T, U.T)
        
        #translation
        t = rotation_center.T - np.dot(rotation_matrix, rotation_center.T)
        
        # homogeneous transformation
        T = np.identity(4)
        T[:3, :3] = rotation_matrix
        T[:3, 3] = t
        
        # rotationTransformNode =  slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode', "svd_rotation_transform")
        # rotationTransformNode.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(T))
        
        return T

    
    def collision_detection(self, plate_node, orbit_node):
        # Variables
        #collisionDetection = vtkSRCP.vtkCollisionDetectionFilter()
        collisionDetection = vtk.vtkCollisionDetectionFilter()
        numberOfCollisions = 0
        collisionFlag = False
        #
        # Collision Detection
        node1ToWorldTransformMatrix = vtk.vtkMatrix4x4()
        node2ToWorldTransformMatrix = vtk.vtkMatrix4x4()
        node1ParentTransformNode = plate_node.GetParentTransformNode()
        node2ParentTransformNode = orbit_node.GetParentTransformNode()
        if node1ParentTransformNode != None:
            node1ParentTransformNode.GetMatrixTransformToWorld(node1ToWorldTransformMatrix)
        if node2ParentTransformNode != None:
            node2ParentTransformNode.GetMatrixTransformToWorld(node2ToWorldTransformMatrix)
        #
        collisionDetection.SetInputData( 0, plate_node.GetPolyData() )
        collisionDetection.SetInputData( 1, orbit_node.GetPolyData() )
        collisionDetection.SetMatrix( 0, node1ToWorldTransformMatrix )
        collisionDetection.SetMatrix( 1, node2ToWorldTransformMatrix )
        collisionDetection.SetBoxTolerance( 0.0 )
        collisionDetection.SetCellTolerance( 0.0 )
        collisionDetection.SetNumberOfCellsPerNode( 2 )
        collisionDetection.Update()
        #
        numberOfCollisions      = collisionDetection.GetNumberOfContacts()
        if numberOfCollisions > 0:
            collisionFlag       = True
        else:
            collisionFlag       = False
        #
        # Status Verbose
        # if(collisionFlag == True ):
        #     print( "{} Collisions Detected".format( numberOfCollisions ) )
        # else:
        #     print( "No Collisions Detected" )
        #
        return collisionFlag, numberOfCollisions
      

    def heatmap(self, templateMesh, currentMesh):
        distanceFilter = vtk.vtkDistancePolyDataFilter()
        distanceFilter.SetInputData(0,templateMesh.GetPolyData())
        distanceFilter.SetInputData(1,currentMesh.GetPolyData())
        # distanceFilter.SetSignedDistance(signedDistanceOption)
        distanceFilter.SignedDistanceOn()
        distanceFilter.Update()
        
        distanceMap = distanceFilter.GetOutput()
        distanceArray = distanceMap.GetPointData().GetArray('Distance')
        #meanDistance = np.average(distanceArray)
        # meanDistance = self.rmse(distanceArray)
        # outputNode=slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode","ouputDistanceMap")
        templateMesh.SetAndObservePolyData(distanceMap)
        return distanceMap, templateMesh



    def intersection_marker(self, plate_model_node, orbit_model_node):
        intersector = vtk.vtkIntersectionPolyDataFilter()
        intersector.SetInputConnection(0,plate_model_node.GetPolyDataConnection())
        intersector.SetInputConnection(1, orbit_model_node.GetPolyDataConnection())
        intersector.Update()

        # intersectionModel = slicer.modules.models.logic().AddModel(intersector.GetOutputDataObject(0))
        # intersectionModel.SetName("intersectionModel_0")
        # intersectionModel.GetDisplayNode().SetColor(0.0, 0.0, 1.0)
        
        return intersector


    # def paint_model_by_volume(self, segmentationNode, masterVolumeNode, InputModelNode, outputModelNode):
    #     #segmentationNode contains plate and orbit segments
    #     #Use Probe Volume with Model
    #     # outputModelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode")
    #     parameters = {}
    #     parameters['InputVolume'] = segmentationNode.GetID()
    #     parameters['InputModel'] = InputModelNode.GetID()
    #     parameters['OutputModel'] = outputModelNode.GetID()
    #     probe = slicer.modules.probevolumewithmodel
    #     slicer.cli.run(probe, None, parameters, wait_for_completion=True)
    #     return
        




    # def getParameterNode(self):
    #     return plateRegistrationParameterNode(super().getParameterNode())

    # def process(self,
    #             inputVolume: vtkMRMLScalarVolumeNode,
    #             outputVolume: vtkMRMLScalarVolumeNode,
    #             imageThreshold: float,
    #             invert: bool = False,
    #             showResult: bool = True) -> None:
    #     """
    #     Run the processing algorithm.
    #     Can be used without GUI widget.
    #     :param inputVolume: volume to be thresholded
    #     :param outputVolume: thresholding result
    #     :param imageThreshold: values above/below this threshold will be set to 0
    #     :param invert: if True then values above the threshold will be set to 0, otherwise values below are set to 0
    #     :param showResult: show output volume in slice viewers
    #     """
    # 
    #     if not inputVolume or not outputVolume:
    #         raise ValueError("Input or output volume is invalid")
    # 
    #     import time
    # 
    #     startTime = time.time()
    #     logging.info("Processing started")
    # 
    #     # Compute the thresholded output volume using the "Threshold Scalar Volume" CLI module
    #     cliParams = {
    #         "InputVolume": inputVolume.GetID(),
    #         "OutputVolume": outputVolume.GetID(),
    #         "ThresholdValue": imageThreshold,
    #         "ThresholdType": "Above" if invert else "Below",
    #     }
    #     cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True, update_display=showResult)
    #     # We don't need the CLI module node anymore, remove it to not clutter the scene with it
    #     slicer.mrmlScene.RemoveNode(cliNode)
    # 
    #     stopTime = time.time()
    #     logging.info(f"Processing completed in {stopTime-startTime:.2f} seconds")


#
# plateRegistrationTest
#


# class plateRegistrationTest(ScriptedLoadableModuleTest):
#     """
#     This is the test case for your scripted module.
#     Uses ScriptedLoadableModuleTest base class, available at:
#     https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
#     """
# 
#     def setUp(self):
#         """Do whatever is needed to reset the state - typically a scene clear will be enough."""
#         slicer.mrmlScene.Clear()
# 
#     def runTest(self):
#         """Run as few or as many tests as needed here."""
#         self.setUp()
#         self.test_plateRegistration1()
# 
#     def test_plateRegistration1(self):
#         """Ideally you should have several levels of tests.  At the lowest level
#         tests should exercise the functionality of the logic with different inputs
#         (both valid and invalid).  At higher levels your tests should emulate the
#         way the user would interact with your code and confirm that it still works
#         the way you intended.
#         One of the most important features of the tests is that it should alert other
#         developers when their changes will have an impact on the behavior of your
#         module.  For example, if a developer removes a feature that you depend on,
#         your test should break so they know that the feature is needed.
#         """
# 
#         self.delayDisplay("Starting the test")
# 
#         # Get/create input data
# 
#         import SampleData
# 
#         registerSampleData()
#         inputVolume = SampleData.downloadSample("plateRegistration1")
#         self.delayDisplay("Loaded test data set")
# 
#         inputScalarRange = inputVolume.GetImageData().GetScalarRange()
#         self.assertEqual(inputScalarRange[0], 0)
#         self.assertEqual(inputScalarRange[1], 695)
# 
#         outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
#         threshold = 100
# 
#         # Test the module logic
# 
#         logic = plateRegistrationLogic()
# 
#         # Test algorithm with non-inverted threshold
#         logic.process(inputVolume, outputVolume, threshold, True)
#         outputScalarRange = outputVolume.GetImageData().GetScalarRange()
#         self.assertEqual(outputScalarRange[0], inputScalarRange[0])
#         self.assertEqual(outputScalarRange[1], threshold)
# 
#         # Test algorithm with inverted threshold
#         logic.process(inputVolume, outputVolume, threshold, False)
#         outputScalarRange = outputVolume.GetImageData().GetScalarRange()
#         self.assertEqual(outputScalarRange[0], inputScalarRange[0])
#         self.assertEqual(outputScalarRange[1], inputScalarRange[1])
# 
#         self.delayDisplay("Test passed")
