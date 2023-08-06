<?xml version='1.0'?>
<datamodel version="6.0" xmlns="http://www.tresos.de/_projects/DataModel2/14/root.xsd" xmlns:a="http://www.tresos.de/_projects/DataModel2/14/attribute.xsd" xmlns:v="http://www.tresos.de/_projects/DataModel2/06/schema.xsd" xmlns:d="http://www.tresos.de/_projects/DataModel2/06/data.xsd">
  <d:ctr type="AUTOSAR" factory="autosar" xmlns:ad="http://www.tresos.de/_projects/DataModel2/08/admindata.xsd" xmlns:cd="http://www.tresos.de/_projects/DataModel2/08/customdata.xsd" xmlns:f="http://www.tresos.de/_projects/DataModel2/14/formulaexpr.xsd" xmlns:icc="http://www.tresos.de/_projects/DataModel2/08/implconfigclass.xsd" xmlns:mt="http://www.tresos.de/_projects/DataModel2/11/multitest.xsd" xmlns:variant="http://www.tresos.de/_projects/DataModel2/11/variant.xsd">
    <d:lst type="TOP-LEVEL-PACKAGES">
      <d:ctr name="#{AR_PACKAGE}" type="AR-PACKAGE">
        <d:lst type="ELEMENTS">
          <d:chc name="#{COMPONENT}" type="AR-ELEMENT" value="MODULE-DEF">
            <v:ctr type="MODULE-DEF">
              <a:a name="ADMIN-DATA" type="ADMIN-DATA">
                <ad:ADMIN-DATA>
                  <ad:LANGUAGE>EN</ad:LANGUAGE>
                  <ad:DOC-REVISIONS>
                    <ad:DOC-REVISION>
                      <ad:REVISION-LABEL>1.0</ad:REVISION-LABEL>
                      <ad:ISSUED-BY>Unknown</ad:ISSUED-BY>
                      <ad:DATE>#{DATE_TIME}</ad:DATE>
                    </ad:DOC-REVISION>
                  </ad:DOC-REVISIONS>
                </ad:ADMIN-DATA>
              </a:a>
              <a:a name="DESC">
                <a:v>FOR-ALL: &lt;html&gt;
                     This container holds the configuration of my complex device driver.
                  &lt;/html&gt;</a:v>
              </a:a>
              <a:a name="RELEASE" value="asc:4.0.0" />
              <v:ctr name="CommonPublishedInformation" type="IDENTIFIABLE">
                <a:a name="DESC">
                  <a:v>EN:
                    &lt;html&gt;
                      Common container, aggregated by all modules. It contains published information about vendor and versions.
                  &lt;/html&gt;</a:v>
                </a:a>
                <a:a name="LABEL" value="Common Published Information"/>
                <v:var name="ArMajorVersion" type="INTEGER_LABEL">
                  <a:a name="DESC">
                    <a:v>EN:
                      &lt;html&gt;
                        Major version number of AUTOSAR specification on which the appropriate implementation is based on.
                    &lt;/html&gt;</a:v>
                  </a:a>
                  <a:a name="IMPLEMENTATIONCONFIGCLASS" 
                       value="PublishedInformation"/>
                  <a:a name="LABEL" value="AUTOSAR Major Version"/>
                  <a:a name="SYMBOLICNAMEVALUE" value="false"/>
                  <a:da name="DEFAULT" value="#{AR_MAJOR}"/>
                </v:var>
                <v:var name="ArMinorVersion" type="INTEGER_LABEL">
                  <a:a name="DESC">
                    <a:v>EN:
                      &lt;html&gt;
                        Minor version number of AUTOSAR specification on which the appropriate implementation is based on.
                    &lt;/html&gt;</a:v>
                  </a:a>
                  <a:a name="IMPLEMENTATIONCONFIGCLASS" 
                       value="PublishedInformation"/>
                  <a:a name="LABEL" value="AUTOSAR Minor Version"/>
                  <a:a name="SYMBOLICNAMEVALUE" value="false"/>
                  <a:da name="DEFAULT" value="#{AR_MINOR}"/>
                </v:var>
                <v:var name="ArPatchVersion" type="INTEGER_LABEL">
                  <a:a name="DESC">
                    <a:v>EN:
                      &lt;html&gt;
                        Patch level version number of AUTOSAR specification on which the appropriate implementation is based on.
                    &lt;/html&gt;</a:v>
                  </a:a>
                  <a:a name="IMPLEMENTATIONCONFIGCLASS" 
                       value="PublishedInformation"/>
                  <a:a name="LABEL" value="AUTOSAR Patch Version"/>
                  <a:a name="SYMBOLICNAMEVALUE" value="false"/>
                  <a:da name="DEFAULT" value="0"/>
                </v:var>
                <v:var name="SwMajorVersion" type="INTEGER_LABEL">
                  <a:a name="DESC">
                    <a:v>EN:
                      &lt;html&gt;
                        Major version number of the vendor specific implementation of the module.
                    &lt;/html&gt;</a:v>
                  </a:a>
                  <a:a name="IMPLEMENTATIONCONFIGCLASS" 
                       value="PublishedInformation"/>
                  <a:a name="LABEL" value="Software Major Version"/>
                  <a:a name="SYMBOLICNAMEVALUE" value="false"/>
                  <a:da name="DEFAULT" value="#{MAJOR}"/>
                </v:var>
                <v:var name="SwMinorVersion" type="INTEGER_LABEL">
                  <a:a name="DESC">
                    <a:v>EN:
                      &lt;html&gt;
                        Minor version number of the vendor specific implementation of the module. The numbering is vendor specific.
                    &lt;/html&gt;</a:v>
                  </a:a>
                  <a:a name="IMPLEMENTATIONCONFIGCLASS" 
                       value="PublishedInformation"/>
                  <a:a name="LABEL" value="Software Minor Version"/>
                  <a:a name="SYMBOLICNAMEVALUE" value="false"/>
                  <a:da name="DEFAULT" value="#{MINOR}"/>
                </v:var>
                <v:var name="SwPatchVersion" type="INTEGER_LABEL">
                  <a:a name="DESC">
                    <a:v>EN:
                      &lt;html&gt;
                        Patch level version number of the vendor specific implementation of the module. The numbering is vendor specific.
                    &lt;/html&gt;</a:v>
                  </a:a>
                  <a:a name="IMPLEMENTATIONCONFIGCLASS" 
                       value="PublishedInformation"/>
                  <a:a name="LABEL" value="Software Patch Version"/>
                  <a:a name="SYMBOLICNAMEVALUE" value="false"/>
                  <a:da name="DEFAULT" value="#{PATCH}"/>
                </v:var>
                <v:var name="ModuleId" type="INTEGER_LABEL">
                  <a:a name="DESC">
                    <a:v>EN:
                      &lt;html&gt;
                        Module ID of this module from Module List
                    &lt;/html&gt;</a:v>
                  </a:a>
                  <a:a name="IMPLEMENTATIONCONFIGCLASS" 
                       value="PublishedInformation"/>
                  <a:a name="LABEL" value="Numeric Module ID"/>
                  <a:a name="SYMBOLICNAMEVALUE" value="false"/>
                  <a:da name="DEFAULT" value="54"/>
                </v:var>
                <v:var name="VendorId" type="INTEGER_LABEL">
                  <a:a name="DESC">
                    <a:v>EN:
                      &lt;html&gt;
                        Vendor ID of the dedicated implementation of this module according to the AUTOSAR vendor list
                    &lt;/html&gt;</a:v>
                  </a:a>
                  <a:a name="IMPLEMENTATIONCONFIGCLASS" 
                       value="PublishedInformation"/>
                  <a:a name="LABEL" value="Vendor ID"/>
                  <a:a name="SYMBOLICNAMEVALUE" value="false"/>
                  <a:da name="DEFAULT" value="1"/>
                </v:var>
                <v:var name="Release" type="STRING_LABEL">
                  <a:a name="IMPLEMENTATIONCONFIGCLASS" 
                       value="PublishedInformation"/>
                  <a:a name="LABEL" value="Release Information"/>
                  <a:a name="ORIGIN" value="Elektrobit Automotive GmbH"/>
                  <a:a name="SYMBOLICNAMEVALUE" value="false"/>
                  <a:da name="DEFAULT" value=""/>
                </v:var>
              </v:ctr>
              <v:var name="IMPLEMENTATION_CONFIG_VARIANT" type="ENUMERATION">
                <a:a name="LABEL" value="Config Variant" />
                <a:da name="DEFAULT" value="VariantPreCompile" />
                <a:da name="RANGE" value="VariantPreCompile" />
              </v:var>
              <v:ctr name="General" type="IDENTIFIABLE">
                <v:var name="Integer" type="INTEGER">
                  <a:a name="ORIGIN" value="EB_Training" />
                  <a:a name="__ORIGIN" value="Training" />
                </v:var>
                <v:var name="Float" type="FLOAT">
                  <a:a name="ORIGIN" value="EB_Training" />
                  <a:a name="__ORIGIN" value="Training" />
                </v:var>
                <v:var name="Boolean" type="BOOLEAN">
                  <a:a name="ORIGIN" value="EB_Training" />
                  <a:a name="__ORIGIN" value="Training" />
                </v:var>
                <v:var name="String" type="STRING">
                  <a:a name="ORIGIN" value="EB_Training" />
                </v:var>
              </v:ctr>
              <v:lst name="#{COMPONENT}TxPduCfg" type="MAP">
                <a:da name="MIN" value="1" />
                <v:ctr name="#{COMPONENT}TxPduCfg" type="IDENTIFIABLE">
                  <v:var name="#{COMPONENT}TxPduId" type="INTEGER">
                    <a:a name="ORIGIN" value="EB_Training" />
                    <a:da name="DEFAULT" value="0" />
                    <a:da name="INVALID" type="Range">
                      <a:tst expr="&lt;=4294967295" />
                      <a:tst expr="&gt;=0" />
                    </a:da>
                  </v:var>
                  <v:ref name="#{COMPONENT}TxPduRef" type="REFERENCE">
                    <a:a name="ORIGIN" value="EB_Training" />
                    <a:da name="REF" value="ASPathDataOfSchema:/AUTOSAR/EcucDefs/EcuC/EcucPduCollection/Pdu" />
                  </v:ref>
                </v:ctr>
              </v:lst>
            </v:ctr>
          </d:chc>
          <d:chc name="myEcuParameterDefinition" type="AR-ELEMENT" value="ECU_PARAMETER_DEFINITION">
            <d:ctr type="AR-ELEMENT">
              <a:a name="DEF" value="ASPath:/AR_PACKAGE_SCHEMA/ECU_PARAMETER_DEFINITION" />
              <d:lst name="MODULE_REF">
                <d:ref type="MODULE_REF" value="ASPath:/{AR_PACKAGE}/#{COMPONENT}" />
              </d:lst>
            </d:ctr>
          </d:chc>
        </d:lst>
      </d:ctr>
    </d:lst>
  </d:ctr>
</datamodel>