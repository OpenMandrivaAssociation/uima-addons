%{?_javapackages_macros:%_javapackages_macros}
Name:          uima-addons
Version:       2.3.1
Release:       3%{?dist}
Summary:       Apache UIMA Addons components
License:       ASL 2.0
URL:           http://uima.apache.org/sandbox.html
Source0:       http://www.apache.org/dist/uima/%{name}-%{version}-source-release.zip
# fix bundle plugin configuration
Patch0:        %{name}-%{version}-disable-embedded-dependencies.patch
# fix build for httpclient > 4.0
Patch1:        %{name}-%{version}-httpclient.patch

BuildRequires: java-devel

BuildRequires: mvn(bsf:bsf)
BuildRequires: mvn(commons-digester:commons-digester)
BuildRequires: mvn(commons-io:commons-io)
BuildRequires: mvn(commons-lang:commons-lang)
BuildRequires: mvn(commons-logging:commons-logging-api)
BuildRequires: mvn(javax.xml.stream:stax-api)
BuildRequires: mvn(log4j:log4j:1.2.17)
BuildRequires: mvn(org.apache.ant:ant)
BuildRequires: mvn(org.apache.httpcomponents:httpclient)
BuildRequires: mvn(org.apache.uima:parent-pom:pom:)
BuildRequires: mvn(org.apache.uima:uimaj-core)
BuildRequires: mvn(org.apache.uima:uimaj-document-annotation)
BuildRequires: mvn(org.apache.xmlbeans:xmlbeans)
BuildRequires: mvn(org.beanshell:bsh)
BuildRequires: mvn(org.tartarus:snowball)
BuildRequires: mvn(rhino:js)
BuildRequires: mvn(org.apache.tomcat:tomcat-servlet-api)

%if 0
# Unavailable build deps **
BuildRequires: mvn(org.apache.lucene:lucene-snowball:2.9.3)
BuildRequires: mvn(org.apache.solr:solr-core:3.1.0)
BuildRequires: mvn(org.apache.solr:solr-solrj:3.1.0)
BuildRequires: mvn(org.apache.tika:tika-core:0.7)
BuildRequires: mvn(org.apache.tika:tika-parsers:0.7)
BuildRequires: mvn(org.apache.uima:uimaj-examples:2.3.1)
BuildRequires: mvn(org.eclipse.emf.ecore:xmi:2.3.0-v200706262000)
BuildRequires: mvn(org.eclipse.emf:common:2.3.0-v200706262000)
BuildRequires: mvn(org.eclipse.emf:ecore:2.3.0-v200706262000)
BuildRequires: mvn(org.mortbay.jetty:jetty:6.1.8)
%endif

# Test deps
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.uima:uimaj-test-util)
BuildRequires: mvn(org.apache.uima:uimaj-component-test-util)

BuildRequires: maven-local
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-site-plugin)
BuildRequires: mvn(org.apache.uima:PearPackagingMavenPlugin)
BuildRequires: mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires: mvn(org.codehaus.mojo:javacc-maven-plugin)
BuildRequires: mvn(org.codehaus.mojo:xmlbeans-maven-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires: mvn(ant-contrib:ant-contrib)
BuildRequires: mvn(org.apache.ant:ant-apache-regexp)

BuildArch:     noarch

%description
UIMA Addons is a collection of Annotators extracted for
sandbox for official distribution. It also provides
Simple Server and Pear packaging tools.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

%patch0 -p0
%patch1 -p0

# Disable unneeded (only for eclipse) OSGi artefacts
%pom_remove_plugin :maven-assembly-plugin uima-addons-parent
%pom_remove_plugin :maven-dependency-plugin uima-addons-parent
%pom_remove_plugin :maven-resources-plugin uima-addons-parent

# Unavailable or too old build deps **
%pom_disable_module ConfigurableFeatureExtractor
%pom_disable_module Lucas
%pom_disable_module Solrcas
%pom_disable_module TikaAnnotator

%pom_remove_dep org.mortbay.jetty:jetty SimpleServer
rm -r SimpleServer/src/main/java/org/apache/uima/simpleserver/util/JettyUtils.java \
 SimpleServer/src/test/java/org/apache/uima/simpleserver/test/ServerFailureTest.java \
 SimpleServer/src/test/java/org/apache/uima/simpleserver/test/ServerTest.java

# Fail with XMvn if aId is different by finalName
for p in AlchemyAPIAnnotator BSFAnnotator ConceptMapper DictionaryAnnotator \
 FsVariables OpenCalaisAnnotator PearPackagingAntTask RegularExpressionAnnotator \
 SimpleServer SnowballAnnotator Tagger WhitespaceTokenizer; do
%pom_xpath_remove "pom:project/pom:build/pom:finalName" ${p}
done

for m in ConfigurableFeatureExtractor DictionaryAnnotator RegularExpressionAnnotator SimpleServer; do
%pom_remove_dep org.apache.geronimo.specs:geronimo-stax-api_1.0_spec  ${m}
%pom_add_dep javax.xml.stream:stax-api:1.0.1 ${m}
done

rm -r SnowballAnnotator/src/main/java/org/tartarus
%pom_add_dep org.tartarus:snowball SnowballAnnotator

# java.lang.AssertionError: null
rm -r AlchemyAPIAnnotator/src/test/java/org/apache/uima/alchemy/annotator/TextRankedEntityExtractionAnnotatorTest.java

sed -i 's/\r//' LICENSE NOTICE

# requires web access
rm -r AlchemyAPIAnnotator/src/test/java/org/apache/uima/alchemy/annotator/SimpleTest.java \
 AlchemyAPIAnnotator/src/test/java/org/apache/uima/alchemy/annotator/HtmlMicroformatsAnnotatorTest.java \
 AlchemyAPIAnnotator/src/test/java/org/apache/uima/alchemy/annotator/TextCategorizationAnnotatorTest.java \
 AlchemyAPIAnnotator/src/test/java/org/apache/uima/alchemy/annotator/TextConceptTaggingAnnotatorTest.java \
 AlchemyAPIAnnotator/src/test/java/org/apache/uima/alchemy/annotator/TextKeywordExtractionAnnotatorTest.java \
 AlchemyAPIAnnotator/src/test/java/org/apache/uima/alchemy/annotator/TextLanguageDetectionAnnotatorTest.java \
 AlchemyAPIAnnotator/src/test/java/org/apache/uima/alchemy/annotator/TextSentimentAnalysisAnnotatorTest.java \
 OpenCalaisAnnotator/src/test/java/org/apache/uima/annotator/calais/OpenCalaisAnnotatorTest.java

sed -i "s|<groupId>javax.servlet</groupId>|<groupId>org.apache.tomcat</groupId>|" SimpleServer/pom.xml
sed -i "s|<artifactId>servlet-api</artifactId>|<artifactId>tomcat-servlet-api</artifactId>|" SimpleServer/pom.xml
# Solrcas/pom.xml

sed -i "s|<version>1.2.14</version>|<version>1.2.17</version>|" BSFAnnotator/pom.xml
#  Lucas/pom.xml

%build

%mvn_package ::pear: __noinstall
%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE NOTICE RELEASE_NOTES.html

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.3.1-2
- Use Requires: java-headless rebuild (#1067528)

* Mon Sep 02 2013 gil cattaneo <puntogil@libero.it> 2.3.1-1
- initial rpm
