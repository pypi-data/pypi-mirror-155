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

#################################################################
# REGISTRY

LIBRARIES_TO_BUILD     += ${COMPONENT}_src

${COMPONENT}_src_FILES += \
${SRC_FILES_TEXT}

#################################################################
# DEPENDENCIES (only for assembler files)
#

#################################################################
# RULES
