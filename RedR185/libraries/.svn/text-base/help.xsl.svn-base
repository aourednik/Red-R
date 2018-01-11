<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h1><xsl:value-of select="documentation/name"/></h1>
  <h2>Summary</h2>
  <p><xsl:copy-of select="documentation/summary"/></p>
<h2>Details</h2>
  <p><xsl:copy-of select="documentation/details" /></p>
    <h2>Signals</h2>
  <table border="1">
    <tr bgcolor="#9acd32">
      <th>Type</th>
      <th>Signal</th>
      <th>Description</th>
    </tr>
    <xsl:for-each select="documentation/signals/input">
    <tr>
      <td>Input</td>
      <td><a href="../../{substring-before(signalClass, ':')}/help/{substring-after(signalClass, ':')}.xml" > <xsl:value-of select="signalClass"/></a></td>
      <td><xsl:value-of select="description"/></td>
    </tr>
    </xsl:for-each>
    <xsl:for-each select="documentation/signals/output">
    <tr>
      <td>Output</td>
      <td><a href="../../{substring-before(signalClass, ':')}/help/{substring-after(signalClass, ':')}.xml" > <xsl:value-of select="signalClass"/></a></td>
      <td><xsl:value-of select="description"/></td>
    </tr>
    </xsl:for-each>
    </table>
    <h2>Parameters</h2>
    <table border="1">
    <tr bgcolor="#9acd32">
      <th>GUI Element</th>
      <th>Name</th>
      <th>Description</th>
    </tr>
    <xsl:for-each select="documentation/GUIElements/parameter">
    <tr>
      <td><xsl:value-of select="element"/></td>
      <td><xsl:value-of select="name"/></td>
      <td><xsl:value-of select="description"/></td>
    </tr>
    </xsl:for-each>
</table>

  </body>
  </html>
</xsl:template>

</xsl:stylesheet>