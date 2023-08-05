A simple export test case
=========================

.. code-block:: python

    >>> from cubicweb import Binary
    >>> record = testutils.authority_record(cnx, u'666', u'Charlie')
    >>> home_addr = cnx.create_entity(
    ...     'PostalAddress', street=u'Place du Capitole',
    ...     postalcode=u'31000', city=u'Toulouse')
    >>> place_entry1 = cnx.create_entity('PlaceEntry', name=u'1')
    >>> place1 = cnx.create_entity(
    ...     'AgentPlace', role=u'home', place_agent=record,
    ...     place_address=home_addr, place_entry_relation=place_entry1)
    >>> work_addr = cnx.create_entity(
    ...     'PostalAddress', street=u'104 bd L.-A. Blanqui',
    ...     postalcode=u'75013', city=u'Paris')
    >>> place_entry2 = cnx.create_entity('PlaceEntry', name=u'2')
    >>> place2 = cnx.create_entity(
    ...     'AgentPlace', role=u'work', place_agent=record,
    ...   place_address=work_addr, place_entry_relation=place_entry2)
    >>> uri = cnx.create_entity('ExternalUri', uri=u'http://www.logilab.fr')
    >>> resource_relation = cnx.create_entity(
    ...     'EACResourceRelation', resource_relation_resource=uri,
    ...     resource_relation_agent=record,
    ...     xml_wrap=Binary(b'<pif><paf>pouf</paf></pif>'))
    >>> record2 = testutils.authority_record(
    ...     cnx, u'2', u'does not matter', kind=u'authority',
    ...     cwuri=u'http://www.example.org/record2')
    >>> chronological_relation = cnx.create_entity(
    ...     'ChronologicalRelation', entry=u'Super Service',
    ...     chronological_predecessor=record2, chronological_successor=record,
    ...     xml_wrap=Binary(b'<plip>plop</plip>'))
    >>> cnx.commit()
    >>> print(record.cw_adapt_to('EAC-CPF').dump().decode().strip())
    <?xml version='1.0' encoding='utf-8'?>
    <eac-cpf xmlns="urn:isbn:1-931666-33-4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="urn:isbn:1-931666-33-4 http://eac.staatsbibliothek-berlin.de/schema/cpf.xsd">
      <control>
        <recordId>666</recordId>
        <maintenanceStatus>new</maintenanceStatus>
        <publicationStatus>inProcess</publicationStatus>
        <maintenanceAgency>
          <agencyName/>
        </maintenanceAgency>
        <languageDeclaration>
          <language languageCode="fre">français</language>
          <script scriptCode="Latn">latin</script>
        </languageDeclaration>
      </control>
      <cpfDescription>
        <identity>
          <entityType>person</entityType>
          <nameEntry>
            <part>Charlie</part>
            <authorizedForm>conventionDeclaration</authorizedForm>
          </nameEntry>
        </identity>
        <description>
          <places>
            <place>
              <placeRole>home</placeRole>
              <placeEntry>1</placeEntry>
              <address>
                <addressLine localType="voie">Place du Capitole</addressLine>
                <addressLine localType="postalcode">31000</addressLine>
                <addressLine localType="city">Toulouse</addressLine>
              </address>
            </place>
            <place>
              <placeRole>work</placeRole>
              <placeEntry>2</placeEntry>
              <address>
                <addressLine localType="voie">104 bd L.-A. Blanqui</addressLine>
                <addressLine localType="postalcode">75013</addressLine>
                <addressLine localType="city">Paris</addressLine>
              </address>
            </place>
          </places>
        </description>
        <relations>
          <cpfRelation cpfRelationType="temporal-earlier" xlink:href="http://www.example.org/record2" xlink:type="simple">
            <relationEntry>Super Service</relationEntry>
            <objectXMLWrap>
              <plip>plop</plip>
            </objectXMLWrap>
          </cpfRelation>
          <resourceRelation xlink:href="http://www.logilab.fr" xlink:type="simple">
            <objectXMLWrap>
              <pif>
                <paf>pouf</paf>
              </pif>
            </objectXMLWrap>
          </resourceRelation>
        </relations>
      </cpfDescription>
    </eac-cpf>
