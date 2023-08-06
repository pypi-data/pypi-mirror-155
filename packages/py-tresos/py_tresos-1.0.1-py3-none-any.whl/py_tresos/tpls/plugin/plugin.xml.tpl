<?xml version="1.0" encoding="UTF-8"?>
<?eclipse version="3.2"?>
<plugin>
   
  <extension point="dreisoft.tresos.launcher2.plugin.module"
             id="#{COMPONENT}_TS_#{VERSION}"
             name="#{COMPONENT}_TS_#{VERSION} Module">

    <module id="#{COMPONENT}_TS_#{VERSION}"
            label="#{COMPONENT}"
            mandatory="false"
            allowMultiple="false"
            description="ECU Information"
            copyright="(c) #{YEAR} #{COMPANY}"
            swVersionMajor="#{MAJOR}"
            swVersionMinor="#{MINOR}"
            swVersionPatch="#{PATCH}"
            specVersionMajor="4"
            specVersionMinor="0"
            specVersionPatch="0"
            specVersionSuffix="0000"
            relVersionMajor="#{AR_MAJOR}"
            relVersionMinor="#{AR_MINOR}"
            relVersionPatch="#{AR_PATCH}"
            categoryType="#{COMPONENT}"
            categoryLayer="Drivers"
            categoryCategory="ECU Firmware"
            categoryComponent="ECUC">
    </module>
  </extension>

    <extension point="dreisoft.tresos.launcher2.plugin.configuration"
             id="#{COMPONENT}_TS_#{VERSION}_ConfigId"
             name="#{COMPONENT}_TS_#{VERSION} Configuration">
    <configuration moduleId="#{COMPONENT}_TS_#{VERSION}">
      <schema>
        <manager class="dreisoft.tresos.autosar2.resourcehandling.AutosarSchemaManager"/>
        <resource value="config/#{COMPONENT}.xdm" type="xdm" id="res_default"/>
      </schema>

      <data>
        <manager class="dreisoft.tresos.autosar2.resourcehandling.AutosarConfigManager"/>
        <schemaNode path="ASPath:/#{AR_PACKAGE}/#{COMPONENT}"/>
      </data>

      <editor id="#{COMPONENT}_TS_#{VERSION}_EditorId"
              label="Default"
              tooltip="ECU Firmware: #{COMPONENT}">
        <class class="dreisoft.tresos.launcher2.editor.GenericConfigEditor">
          <parameter name="schema" value="ASPath:/#{AR_PACKAGE}/#{COMPONENT}"/>
          <parameter name="title" value="#{COMPONENT}"/>
          <parameter name="noTabs" value="false"/>
          <parameter name="noLinks" value="true"/>
          <parameter name="groupLinks" value="false"/>
          <parameter name="groupContainers" value="false"/>
          <parameter name="groupTables" value="true"/>
          <parameter name="optionalGeneralTab" value="true"/>
        </class>
      </editor>
    </configuration>
  </extension>
    <extension
          id="#{COMPONENT}_TS_#{VERSION}_GeneratorId"
          name="#{COMPONENT}_TS_#{VERSION} Generator"
          point="dreisoft.tresos.launcher2.plugin.generator">
       <generator
             class="dreisoft.tresos.launcher2.generator.TemplateBasedCodeGenerator"
             id="#{COMPONENT}_TemplateBaseCodeGenerator"
             moduleId="#{COMPONENT}_TS_#{VERSION}">
             
          <!-- common template path parameters -->
	      <parameter name="templates"
	                 mode="generate,verify" value="generate"/>
	
	      <!-- swcd modes and template path parameters -->
	      <parameter name="mode_type"
	                 mode="generate_swcd" value="generate"/>
	
	      <parameter name="mode_type"
	                 mode="verify_swcd" value="verify"/>
	
	      <parameter name="templates"
	                 mode="generate_swcd,verify_swcd" value="generate_swcd"/>

       </generator>
     
    </extension>
</plugin>
