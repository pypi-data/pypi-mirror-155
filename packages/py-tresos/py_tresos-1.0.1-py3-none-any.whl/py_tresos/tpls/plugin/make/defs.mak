# \file
#
# \brief ECU_Firmware ${COMPONENT}
#
# This file contains the implementation of the ECU_Firmware
# module ${COMPONENT}.
#
# \author ${AUTHOR}
#
# Copyright ${YEAR} ${COMPANY}
# All rights exclusively reserved for ${COMPANY},
# unless expressly agreed to otherwise.

#################################################################
# DEFINITIONS

${COMPONENT}_CORE_PATH      ?= $$(PLUGINS_BASE)/${COMPONENT}_$$(${COMPONENT}_VARIANT)

${COMPONENT}_OUTPUT_PATH    ?= $$(AUTOSAR_BASE_OUTPUT_PATH)

${COMPONENT}_GEN_FILES = \
${GEN_FILES_TEXT}

TRESOS_GEN_FILES   += $$(${COMPONENT}_GEN_FILES)

CC_INCLUDE_PATH    += \
	$$(${COMPONENT}_CORE_PATH)/include \
	$$(${COMPONENT}_OUTPUT_PATH)/include