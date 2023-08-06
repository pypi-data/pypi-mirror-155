<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<project default="copy_files" name="#{COMPONENT}">
	<property name="project_name" value="#{COMPONENT}_TS_#{VERSION}" />
	<!--this file was created by Eclipse Runnable JAR Export Wizard-->
	<!--ANT 1.7 is required                                        -->
	<!--define folder properties-->
	<property name="dir.tresos" value="#{TRESOS_ROOT}" />
	<property name="dir.plugins" value="${dir.tresos}/plugins" />
	<property name="dir.workspace" value="${dir.buildfile}/.." />
	<property name="dir.jarfile" value="${dir.buildfile}" />
	<target name="copy_files">
		<copy todir="${dir.plugins}/${project_name}" flatten="false">
			<path>
			    <pathelement path="${java.class.path}"/>
			  </path>
			<fileset dir="${dir.workspace}">
				<include name="src/**"/>
				<include name="include/**"/>
				<include name="config/**"/>
				<include name="build/**"/>
				<include name="doc/**"/>
				<include name="generate/**"/>
				<include name="generate_swcd/**"/>
				<include name="make/**"/>
				<include name="META-INF/**"/>
				<include name="plugin.xml"/>
			</fileset>
		</copy>
	</target>
</project>
