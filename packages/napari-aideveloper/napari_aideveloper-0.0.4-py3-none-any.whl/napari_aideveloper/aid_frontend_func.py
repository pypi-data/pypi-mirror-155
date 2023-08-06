#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 15:14:19 2022

@author: nana
"""
from pyqtgraph.Qt import QtCore, QtWidgets
import numpy as np
import ast

def message(msg_text,msg_type="Error"):
    #There was an error!
    msg = QtWidgets.QMessageBox()
    if msg_type=="Error":
        msg.setIcon(QtWidgets.QMessageBox.Critical)       
    elif msg_type=="Information":
        msg.setIcon(QtWidgets.QMessageBox.Information)       
    elif msg_type=="Question":
        msg.setIcon(QtWidgets.QMessageBox.Question)       
    elif msg_type=="Warning":
        msg.setIcon(QtWidgets.QMessageBox.Warning)       
    msg.setText(str(msg_text))
    msg.setWindowTitle(msg_type)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()
    pass

def load_hyper_params(ui_item,para):
    if para["new_model"].iloc[-1]==True:
        ui_item.radioButton_NewModel.setChecked(True)
        prop = str(para["Chosen Model"].iloc[-1])
        index = ui_item.comboBox_ModelSelection.findText(prop, QtCore.Qt.MatchFixedString)
        if index >= 0:
            ui_item.comboBox_ModelSelection.setCurrentIndex(index)
    elif para["loadrestart_model"].iloc[-1]==True:
        ui_item.radioButton_NewModel.setChecked(True)
        prop = str(para["Continued_Fitting_From"])
        ui_item.lineEdit_LoadModelPath.setText(prop)
    elif para["loadcontinue_model"].iloc[-1]==True:
        ui_item.radioButton_LoadContinueModel.setChecked(True)
        prop = str(para["Continued_Fitting_From"].iloc[-1])
        ui_item.lineEdit_LoadModelPath.setText(prop)
    if "Input image size" in para.keys():
        prop = para["Input image size"].iloc[-1]
    elif "Input image crop" in para.keys():
        prop = para["Input image crop"].iloc[-1]
    else:
        prop = 32
        print("Cound not find parameter for 'Input image size' in the meta file")
    ui_item.spinBox_imagecrop.setValue(prop)
    try:
        prop = para["Color Mode"].iloc[-1]
        index = ui_item.comboBox_GrayOrRGB.findText(prop, QtCore.Qt.MatchFixedString)
        if index >= 0:
            ui_item.comboBox_GrayOrRGB.setCurrentIndex(index)
    except Exception as e:
        message(e)
    try:
        prop = int(para["Zoom order"].iloc[-1])
        ui_item.comboBox_zoomOrder.setCurrentIndex(prop)
    except Exception as e:
        message(e)
    try:
        prop = str(para["Normalization"].iloc[-1])
        index = ui_item.comboBox_Normalization.findText(prop, QtCore.Qt.MatchFixedString)
        if index >= 0:
            ui_item.comboBox_Normalization.setCurrentIndex(index)
    except Exception as e:
        message(e)
    try:
        prop = int(para["Nr. epochs"].iloc[-1])
        ui_item.spinBox_NrEpochs.setValue(prop)
    except Exception as e:
        message(e)
    try:
        prop = int(para["Keras refresh after nr. epochs"].iloc[-1])
        ui_item.spinBox_RefreshAfterEpochs.setValue(prop)
        prop = bool(para["Horz. flip"].iloc[-1])
        ui_item.checkBox_HorizFlip.setChecked(prop)
        prop = bool(para["Vert. flip"].iloc[-1])
        ui_item.checkBox_HorizFlip.setChecked(prop)
        prop = str(para["rotation"].iloc[-1])
        ui_item.lineEdit_Rotation.setText(prop)
        prop = str(para["width_shift"].iloc[-1])
        ui_item.lineEdit_widthShift.setText(prop)
        prop = str(para["height_shift"].iloc[-1])
        ui_item.lineEdit_heightShift.setText(prop)
        prop = str(para["zoom"].iloc[-1])
        ui_item.lineEdit_zoomRange.setText(prop)
        prop = str(para["shear"].iloc[-1])
        ui_item.lineEdit_shearRange.setText(prop)
    except Exception as e:
        message(e)
    try:    
        prop = int(para["Keras refresh after nr. epochs"].iloc[-1])
        ui_item.spinBox_RefreshAfterNrEpochs.setValue(prop)
        prop = int(para["Brightness add. lower"].iloc[-1])
        ui_item.spinBox_PlusLower.setValue(prop)
        prop = int(para["Brightness add. upper"].iloc[-1])
        ui_item.spinBox_PlusUpper.setValue(prop)
        prop = float(para["Brightness mult. lower"].iloc[-1])
        ui_item.doubleSpinBox_MultLower.setValue(prop)
        prop = float(para["Brightness mult. upper"].iloc[-1])
        ui_item.doubleSpinBox_MultUpper.setValue(prop)
        prop = float(para["Gaussnoise Mean"].iloc[-1])
        ui_item.doubleSpinBox_GaussianNoiseMean.setValue(prop)
        prop = float(para["Gaussnoise Scale"].iloc[-1])
        ui_item.doubleSpinBox_GaussianNoiseScale.setValue(prop)
    except Exception as e:
        message(e)
    try:
        prop = bool(para["Contrast on"].iloc[-1])
        ui_item.checkBox_contrast.setChecked(prop)
        prop = float(para["Contrast Lower"].iloc[-1])
        ui_item.doubleSpinBox_contrastLower.setValue(prop)
        prop = float(para["Contrast Higher"].iloc[-1])
        ui_item.doubleSpinBox_contrastHigher.setValue(prop)
        prop = bool(para["Saturation on"].iloc[-1])
        ui_item.checkBox_saturation.setChecked(prop)
        prop = float(para["Saturation Lower"].iloc[-1])
        ui_item.doubleSpinBox_saturationLower.setValue(prop)
        prop = float(para["Saturation Higher"].iloc[-1])
        ui_item.doubleSpinBox_saturationHigher.setValue(prop)
        prop = bool(para["Hue on"].iloc[-1])
        ui_item.checkBox_hue.setChecked(prop)
        prop = float(para["Hue delta"].iloc[-1])
        ui_item.doubleSpinBox_hueDelta.setValue(prop)
    except Exception as e:
        message(e)
    try:
        prop = bool(para["Average blur on"].iloc[-1])
        ui_item.checkBox_avgBlur.setChecked(prop)
        prop = int(para["Average blur Lower"].iloc[-1])
        ui_item.spinBox_avgBlurMin.setValue(prop)
        prop = int(para["Average blur Higher"].iloc[-1])
        ui_item.spinBox_avgBlurMax.setValue(prop)
        prop = bool(para["Gauss blur on"].iloc[-1])
        ui_item.checkBox_gaussBlur.setChecked(prop)
        prop = int(para["Gauss blur Lower"].iloc[-1])
        ui_item.spinBox_gaussBlurMin.setValue(prop)
        prop = int(para["Gauss blur Higher"].iloc[-1])
        ui_item.spinBox_gaussBlurMax.setValue(prop)
        prop = bool(para["Motion blur on"].iloc[-1])
        ui_item.checkBox_motionBlur.setChecked(prop)
        prop = str(para["Motion blur Kernel"].iloc[-1])
        ui_item.lineEdit_motionBlurKernel.setText(prop)
        prop = str(para["Motion blur Angle"].iloc[-1])
        ui_item.lineEdit_motionBlurAngle.setText(prop)
    except Exception as e:
        message(e)
    try:
        prop = bool(para["expert_mode"].iloc[-1])
        ui_item.groupBox_expertMode.setChecked(prop)
    except Exception as e:
        message(e)
    try:
        prop = str(para["optimizer_settings"].iloc[-1])
        prop = eval(prop)
        ui_item.optimizer_settings["doubleSpinBox_lr_sgd"] = prop["doubleSpinBox_lr_sgd"]
        ui_item.optimizer_settings["doubleSpinBox_sgd_momentum"] = prop["doubleSpinBox_sgd_momentum"]
        ui_item.optimizer_settings["checkBox_sgd_nesterov"] = prop["checkBox_sgd_nesterov"]
    
        ui_item.optimizer_settings["doubleSpinBox_lr_rmsprop"] = prop["doubleSpinBox_lr_rmsprop"]
        ui_item.optimizer_settings["doubleSpinBox_rms_rho"] = prop["doubleSpinBox_rms_rho"]
    
        ui_item.optimizer_settings["doubleSpinBox_lr_adam"] = prop["doubleSpinBox_lr_adam"]
        ui_item.optimizer_settings["doubleSpinBox_adam_beta1"] = prop["doubleSpinBox_adam_beta1"]
        ui_item.optimizer_settings["doubleSpinBox_adam_beta2"] = prop["doubleSpinBox_adam_beta2"]
        ui_item.optimizer_settings["checkBox_adam_amsgrad"] = prop["checkBox_adam_amsgrad"]
    
        ui_item.optimizer_settings["doubleSpinBox_lr_adadelta"] = prop["doubleSpinBox_lr_adadelta"]
        ui_item.optimizer_settings["doubleSpinBox_adadelta_rho"] = prop["doubleSpinBox_adadelta_rho"]
    
        ui_item.optimizer_settings["doubleSpinBox_lr_nadam"] = prop["doubleSpinBox_lr_nadam"]
        ui_item.optimizer_settings["doubleSpinBox_nadam_beta1"] = prop["doubleSpinBox_nadam_beta1"]
        ui_item.optimizer_settings["doubleSpinBox_nadam_beta2"] = prop["doubleSpinBox_nadam_beta2"]
    
        ui_item.optimizer_settings["doubleSpinBox_lr_adagrad"] = prop["doubleSpinBox_lr_adagrad"]
    
        ui_item.optimizer_settings["doubleSpinBox_lr_adamax"] = prop["doubleSpinBox_lr_adamax"]
        ui_item.optimizer_settings["doubleSpinBox_adamax_beta1"] = prop["doubleSpinBox_adamax_beta1"]
        ui_item.optimizer_settings["doubleSpinBox_adamax_beta2"] = prop["doubleSpinBox_adamax_beta2"]
    except Exception as e:
        message(e)
    try:
        prop = bool(para["optimizer_expert_on"].iloc[-1])
        ui_item.checkBox_optimizer.setChecked(prop)
        prop = str(para["optimizer_expert"].iloc[-1])
        index = ui_item.comboBox_optimizer.findText(prop, QtCore.Qt.MatchFixedString)
        if index >= 0:
            ui_item.comboBox_optimizer.setCurrentIndex(index)
    except Exception as e:
        message(e)
    try:
        prop = int(para["batchSize_expert"].iloc[-1])
        ui_item.spinBox_batchSize.setValue(prop)
        prop = int(para["epochs_expert"].iloc[-1])
        ui_item.spinBox_epochs.setValue(prop)
    except Exception as e:
        message(e)
    try:
        prop = bool(para["learning_rate_expert_on"].iloc[-1])
        ui_item.groupBox_learningRate.setChecked(prop)
    except Exception as e:
        message(e)
    try:
        prop = bool(para["learning_rate_const_on"].iloc[-1])
        ui_item.radioButton_LrConst.setChecked(prop)
        prop = float(para["learning_rate_const"].iloc[-1])
        ui_item.doubleSpinBox_learningRate.setValue(prop)
    except Exception as e:
        message(e)
    try:
        prop = bool(para["learning_rate_cycLR_on"].iloc[-1])
        ui_item.radioButton_LrCycl.setChecked(prop)
        prop = str(para["cycLrMin"].iloc[-1])
        ui_item.lineEdit_cycLrMin.setText(prop)
        prop = str(para["cycLrMax"].iloc[-1])
        ui_item.lineEdit_cycLrMax.setText(prop)
        prop = str(para["cycLrMethod"].iloc[-1])
        index = ui_item.comboBox_cycLrMethod.findText(prop, QtCore.Qt.MatchFixedString)
        if index >= 0:
            ui_item.comboBox_cycLrMethod.setCurrentIndex(index)
        prop = str(para["clr_settings"].iloc[-1])
        prop = eval(prop)
        ui_item.clr_settings["step_size"] = prop["step_size"]
        ui_item.clr_settings["gamma"] = prop["gamma"]
    except Exception as e:
        message(e)
    try:
        prop = bool(para["learning_rate_expo_on"].iloc[-1])
        ui_item.radioButton_LrExpo.setChecked(prop)
        prop = float(para["expDecInitLr"].iloc[-1])
        ui_item.doubleSpinBox_expDecInitLr.setValue(prop)
        prop = int(para["expDecSteps"].iloc[-1])
        ui_item.spinBox_expDecSteps.setValue(prop)
        prop = float(para["expDecRate"].iloc[-1])
        ui_item.doubleSpinBox_expDecRate.setValue(prop)
    except Exception as e:
        message(e)
    try:
        prop = bool(para["loss_expert_on"].iloc[-1])
        ui_item.checkBox_expt_loss.setChecked(prop)
        prop = str(para["loss_expert"].iloc[-1])
        index = ui_item.comboBox_expt_loss.findText(prop, QtCore.Qt.MatchFixedString)
        if index >= 0:
            ui_item.comboBox_expt_loss.setCurrentIndex(index)
    except Exception as e:
        message(e)
    try:
        prop = str(para["paddingMode"].iloc[-1])
        index = ui_item.comboBox_paddingMode.findText(prop, QtCore.Qt.MatchFixedString)
        if index >= 0:
            ui_item.comboBox_paddingMode.setCurrentIndex(index)
    except Exception as e:
        message(e)
    try:
        prop = bool(para["train_last_layers"].iloc[-1])
        ui_item.checkBox_trainLastNOnly.setChecked(prop)
        prop = int(para["train_last_layers_n"].iloc[-1])
        ui_item.spinBox_trainLastNOnly.setValue(prop)
        prop = bool(para["train_dense_layers"].iloc[-1])
        ui_item.checkBox_trainDenseOnly.setChecked(prop)
    except Exception as e:
        message(e)
    try:
        prop = bool(para["dropout_expert_on"].iloc[-1])
        ui_item.checkBox_dropout.setChecked(prop)
        prop = str(para["dropout_expert"].iloc[-1])
        if prop!="()":
            ui_item.lineEdit_dropout.setText(prop[1:-1])
    except Exception as e:
        message(e)
    try:
        prop = bool(para["lossW_expert_on"].iloc[-1])
        ui_item.checkBox_lossW.setChecked(prop)
        prop = str(para["lossW_expert"].iloc[-1])
        if prop!="nan":
            ui_item.lineEdit_lossW.setText(prop)
    except Exception as e:
        message(e)
    try:
        prop = str(para["metrics"].iloc[-1])
        if "accuracy" in prop.lower():
            ui_item.checkBox_expertAccuracy.setChecked(True)
        if "auc" in prop.lower():
            ui_item.checkBox_expertF1.setChecked(True)
        if "precision" in prop.lower():
            ui_item.checkBox_expertPrecision.setChecked(True)
        if "recall" in prop.lower():
            ui_item.checkBox_expertRecall.setChecked(True)
    except Exception as e:
        message(e)


def get_hyper_params(Para_dict,ui_item):
    Para_dict["Modelname"]=str(ui_item.lineEdit_modelname.text()),
    Para_dict["Chosen Model"]=str(ui_item.comboBox_ModelSelection.currentText()),
    Para_dict["new_model"]=ui_item.radioButton_NewModel.isChecked(),
    Para_dict["loadrestart_model"]=ui_item.radioButton_LoadRestartModel.isChecked(),
    Para_dict["loadcontinue_model"]=ui_item.radioButton_LoadContinueModel.isChecked(),
    if ui_item.radioButton_LoadRestartModel.isChecked():
        load_modelname = str(ui_item.lineEdit_LoadModelPath.text())
    elif ui_item.radioButton_LoadContinueModel.isChecked():
        load_modelname = str(ui_item.lineEdit_LoadModelPath.text())
    elif ui_item.radioButton_NewModel.isChecked():
        load_modelname = "" #No model is loaded
    else:
        load_modelname = ""
    Para_dict["Continued_Fitting_From"]=load_modelname,                        
    Para_dict["Input image size"]=int(ui_item.spinBox_imagecrop.value()) ,
    Para_dict["Color Mode"]=str(ui_item.comboBox_GrayOrRGB.currentText()),
    try: Para_dict["Zoom order"]=int(ui_item.comboBox_zoomOrder.currentIndex()), 
    except Exception as e:
        message(e)
    try:
        if ui_item.radioButton_cpu.isChecked():
            gpu_used = False
            deviceSelected = str(ui_item.comboBox_cpu.currentText())
        elif ui_item.radioButton_gpu.isChecked():
            gpu_used = True
            deviceSelected = str(ui_item.comboBox_gpu.currentText())
        gpu_memory = float(ui_item.doubleSpinBox_memory.value())
        Para_dict["Device"]=deviceSelected,
        Para_dict["gpu_used"]=gpu_used,
        Para_dict["gpu_memory"]=gpu_memory,
    except Exception as e:
        message(e)
    Para_dict["Output Nr. classes"]=np.nan,
    norm = str(ui_item.comboBox_Normalization.currentText())
    Para_dict["Normalization"]=norm,
    Para_dict["Nr. epochs"]=int(ui_item.spinBox_NrEpochs.value()),
    try:
        Para_dict["Keras refresh after nr. epochs"]=int(ui_item.spinBox_RefreshAfterEpochs.value()),
        Para_dict["Horz. flip"]= bool(ui_item.checkBox_HorizFlip.isChecked()),
        Para_dict["Vert. flip"]= bool(ui_item.checkBox_VertFlip.isChecked()),
        Para_dict["rotation"]=float(ui_item.lineEdit_Rotation.text()),
        Para_dict["width_shift"]=float(ui_item.lineEdit_widthShift.text()),
        Para_dict["height_shift"]=float(ui_item.lineEdit_heightShift.text()),
        Para_dict["zoom"]=float(ui_item.lineEdit_zoomRange.text()),
        Para_dict["shear"]=float(ui_item.lineEdit_shearRange.text()),
    except Exception as e:
        message(e)
    try:
        Para_dict["Brightness refresh after nr. epochs"]=int(ui_item.spinBox_RefreshAfterNrEpochs.value()),
        Para_dict["Brightness add. lower"]=float(ui_item.spinBox_PlusLower.value()),
        Para_dict["Brightness add. upper"]=float(ui_item.spinBox_PlusUpper.value()),
        Para_dict["Brightness mult. lower"]=float(ui_item.doubleSpinBox_MultLower.value()),  
        Para_dict["Brightness mult. upper"]=float(ui_item.doubleSpinBox_MultUpper.value()),
        Para_dict["Gaussnoise Mean"]=float(ui_item.doubleSpinBox_GaussianNoiseMean.value()),
        Para_dict["Gaussnoise Scale"]=float(ui_item.doubleSpinBox_GaussianNoiseScale.value()),
    except Exception as e:
        message(e)
    try:
        Para_dict["Contrast on"]=bool(ui_item.checkBox_contrast.isChecked()) ,                
        Para_dict["Contrast Lower"]=float(ui_item.doubleSpinBox_contrastLower.value()),
        Para_dict["Contrast Higher"]=float(ui_item.doubleSpinBox_contrastHigher.value()),
        Para_dict["Saturation on"]=bool(ui_item.checkBox_saturation.isChecked()),
        Para_dict["Saturation Lower"]=float(ui_item.doubleSpinBox_saturationLower.value()),
        Para_dict["Saturation Higher"]=float(ui_item.doubleSpinBox_saturationHigher.value()),
        Para_dict["Hue on"]=bool(ui_item.checkBox_hue.isChecked()),                
        Para_dict["Hue delta"]=float(ui_item.doubleSpinBox_hueDelta.value()),                
    except Exception as e:
        message(e)
    try:
        Para_dict["Average blur on"]=bool(ui_item.checkBox_avgBlur.isChecked()),                
        Para_dict["Average blur Lower"]=int(ui_item.spinBox_avgBlurMin.value()),
        Para_dict["Average blur Higher"]=int(ui_item.spinBox_avgBlurMax.value()),
        Para_dict["Gauss blur on"]= bool(ui_item.checkBox_gaussBlur.isChecked()) ,                
        Para_dict["Gauss blur Lower"]=int(ui_item.spinBox_gaussBlurMin.value()),
        Para_dict["Gauss blur Higher"]=int(ui_item.spinBox_gaussBlurMax.value()),
    except Exception as e:
        message(e)
    try:
        Para_dict["Motion blur on"]=bool(ui_item.checkBox_motionBlur.isChecked()),
        motionBlur_kernel = str(ui_item.lineEdit_motionBlurKernel.text())
        motionBlur_angle = str(ui_item.lineEdit_motionBlurAngle.text())
        motionBlur_kernel = tuple(ast.literal_eval(motionBlur_kernel)) #translate string in the lineEdits to a tuple
        motionBlur_angle = tuple(ast.literal_eval(motionBlur_angle)) #translate string in the lineEdits to a tuple
        Para_dict["Motion blur Kernel"]=motionBlur_kernel,               
        Para_dict["Motion blur Angle"]=motionBlur_angle,          
    except Exception as e:
        message(e)

    Para_dict["Epoch_Started_Using_These_Settings"]=np.nan,
    try:
        Para_dict["expert_mode"]=bool(ui_item.groupBox_expertMode.isChecked()),
        Para_dict["batchSize_expert"]=int(ui_item.spinBox_batchSize.value()),
        Para_dict["epochs_expert"]=int(ui_item.spinBox_epochs.value()),
    except Exception as e:
        message(e)
    try:
        Para_dict["learning_rate_expert_on"]=bool(ui_item.groupBox_learningRate.isChecked()),
        Para_dict["learning_rate_const_on"]=bool(ui_item.radioButton_LrConst.isChecked()),
        Para_dict["learning_rate_const"]=float(ui_item.doubleSpinBox_learningRate.value()),
        Para_dict["learning_rate_cycLR_on"]=bool(ui_item.radioButton_LrCycl.isChecked()),
    except Exception as e:
        message(e)
    try:
        Para_dict["cycLrMin"]=float(ui_item.lineEdit_cycLrMin.text()),
        Para_dict["cycLrMax"]=float(ui_item.lineEdit_cycLrMax.text()),
    except:
        Para_dict["cycLrMin"]=np.nan,
        Para_dict["cycLrMax"]=np.nan,
    try:
        Para_dict["cycLrMethod"] = str(ui_item.comboBox_cycLrMethod.currentText()),
        Para_dict["clr_settings"] = ui_item.clr_settings,
    except Exception as e:
        message(e)
    try:
        Para_dict["learning_rate_expo_on"]=bool(ui_item.radioButton_LrExpo.isChecked()) ,
        Para_dict["expDecInitLr"]=float(ui_item.doubleSpinBox_expDecInitLr.value()),
        Para_dict["expDecSteps"]=int(ui_item.spinBox_expDecSteps.value()),
        Para_dict["expDecRate"]=float(ui_item.doubleSpinBox_expDecRate.value()),
    except Exception as e:
        message(e)
    try:
        Para_dict["loss_expert_on"]= bool(ui_item.checkBox_expt_loss.isChecked()),
        Para_dict["loss_expert"]=str(ui_item.comboBox_expt_loss.currentText()).lower(),
        Para_dict["optimizer_expert_on"]=bool(ui_item.checkBox_optimizer.isChecked()),
        Para_dict["optimizer_expert"]=str(ui_item.comboBox_optimizer.currentText()).lower(),                
        Para_dict["optimizer_settings"]=ui_item.optimizer_settings,                
    except Exception as e:
        message(e)
    try:
        Para_dict["paddingMode"]=str(ui_item.comboBox_paddingMode.currentText())#.lower(),                
    except Exception as e:
        message(e)
    try:
        Para_dict["train_last_layers"]=bool(ui_item.checkBox_trainLastNOnly.isChecked()),
        Para_dict["train_last_layers_n"]=int(ui_item.spinBox_trainLastNOnly.value())     ,
        Para_dict["train_dense_layers"]=bool(ui_item.checkBox_trainDenseOnly.isChecked()),
        Para_dict["dropout_expert_on"]=bool(ui_item.checkBox_dropout.isChecked()),
    except Exception as e:
        message(e)
    try:
        dropout_expert = str(ui_item.lineEdit_dropout.text()) #due to the validator, there are no squ.brackets
        dropout_expert = "["+dropout_expert+"]"
        dropout_expert = ast.literal_eval(dropout_expert)        
    except:
        dropout_expert = []
    try:
        Para_dict["dropout_expert"]=dropout_expert,
        Para_dict["lossW_expert_on"]=bool(ui_item.checkBox_lossW.isChecked()),
    except Exception as e:
        message(e)
    try:
        lossW_expert = str(ui_item.lineEdit_lossW.text())
        SelectedFiles = ui_item.items_clicked()
        class_weight = ui_item.get_class_weight(SelectedFiles,str(ui_item.lineEdit_lossW.text()),custom_check_classes=True)
        if type(class_weight)==list:
            #There has been a mismatch between the classes described in class_weight and the classes available in SelectedFiles!
            lossW_expert = class_weight[0] #overwrite 
            class_weight = class_weight[1]
            print("class_weight:" +str(class_weight))
            print("There has been a mismatch between the classes described in \
                  Loss weights and the classes available in the selected files! \
                  Hence, the Loss weights are set to Balanced")
        Para_dict["lossW_expert"]=lossW_expert,
        Para_dict["class_weight"]=class_weight,
    except Exception as e:
        message(e)
    try:
        Para_dict["metrics"]=ui_item.get_metrics(),       
        if norm == "StdScaling using mean and std of all training data":                                
            #This needs to be saved into Para_dict since it will be required for inference
            Para_dict["Mean of training data used for scaling"]=np.nan,
            Para_dict["Std of training data used for scaling"]=np.nan,
    except Exception as e:
        message(e)

    return Para_dict

