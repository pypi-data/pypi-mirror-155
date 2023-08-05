# coding: utf-8
# copyright 2015-2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-eac unit tests for dataimport"""

import datetime
from io import BytesIO
from itertools import count
from os.path import join, dirname
import unittest

from lxml import etree

from cubicweb import NoResultError
from cubicweb.dataimport.importer import ExtEntity, SimpleImportLog
from cubicweb.devtools.testlib import CubicWebTC

from cubicweb_eac import dataimport, testutils

XML_TEST = """
<note test="test_value" test2="test2_value">
<to>Tove</to>
<from>Jani</from>
<heading>Reminder</heading>
<body>Hey!</body>
<empty></empty>
</note>
"""


def mock_(string):
    return string


def tolist(dic):
    """Transform sets in `dic` values as lists for easier comparison."""
    for k, v in dic.items():
        if isinstance(v, set):
            v = list(v)
        dic[k] = v
    return dic


def extentities2dict(entities):
    edict = {}
    for extentity in entities:
        edict.setdefault(extentity.etype, {})[extentity.extid] = extentity.values
    return edict


class EACXMLParserTC(unittest.TestCase):
    @classmethod
    def datapath(cls, *fname):
        """joins the object's datadir and `fname`"""
        return join(dirname(__file__), "data", *fname)

    def file_extentities(self, fname):
        fpath = self.datapath(fname)
        import_log = SimpleImportLog(fpath)
        # Use a predictable extid_generator.
        extid_generator = map(str, count()).__next__
        importer = dataimport.EACCPFImporter(
            fpath, import_log, mock_, extid_generator=extid_generator
        )
        return importer.external_entities()

    def test_parse_FRAD033_EAC_00001(self):
        _gen_extid = map(str, (x for x in count() if x not in (2, 38))).__next__
        expected = [
            (
                "EACOtherRecordId",
                _gen_extid(),
                {
                    "eac_other_record_id_of": set(
                        ["authorityrecord-FRAD033_EAC_00001"]
                    ),
                    "value": set(["1234"]),
                },
            ),
            (
                "EACOtherRecordId",
                _gen_extid(),
                {
                    "eac_other_record_id_of": set(
                        ["authorityrecord-FRAD033_EAC_00001"]
                    ),
                    "value": set(["ABCD"]),
                    "local_type": set(["letters"]),
                },
            ),
            (
                "EACSource",
                _gen_extid(),
                {
                    "source_agent": set(["authorityrecord-FRAD033_EAC_00001"]),
                    "title": set(["1. Ouvrages imprimés..."]),
                    "description": set(["des bouquins"]),
                    "description_format": set(["text/plain"]),
                },
            ),
            (
                "EACSource",
                _gen_extid(),
                {
                    "source_agent": set(["authorityrecord-FRAD033_EAC_00001"]),
                    "url": set(["http://archives.gironde.fr"]),
                    "title": set(["Site des Archives départementales de la Gironde"]),
                },
            ),
            (
                "Activity",
                _gen_extid(),
                {
                    "type": set(["create"]),
                    "agent_type": ["human"],
                    "generated": set(["authorityrecord-FRAD033_EAC_00001"]),
                    "start": set([datetime.datetime(2013, 4, 24, 5, 34, 41)]),
                    "end": set([datetime.datetime(2013, 4, 24, 5, 34, 41)]),
                    "description": set(["bla bla"]),
                    "description_format": set(["text/plain"]),
                },
            ),
            (
                "Activity",
                _gen_extid(),
                {
                    "generated": set(["authorityrecord-FRAD033_EAC_00001"]),
                    "type": set(["modify"]),
                    "agent_type": ["human"],
                    "start": set([datetime.datetime(2015, 1, 15, 7, 16, 33)]),
                    "end": set([datetime.datetime(2015, 1, 15, 7, 16, 33)]),
                    "agent": set(["Delphine Jamet"]),
                },
            ),
            (
                "Convention",
                _gen_extid(),
                {
                    "convention_of": ["authorityrecord-FRAD033_EAC_00001"],
                    "abbrev": set(["ISAAR(CPF)"]),
                    "has_citation": ["8"],
                    "description_format": set(["text/html"]),
                    "description": set(
                        [
                            '<p xmlns="urn:isbn:1-931666-33-4" '
                            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                            'xmlns:xlink="http://www.w3.org/1999/xlink">Norme '
                            "ISAAR(CPF) du Conseil international des archives, "
                            "2e \xe9dition, 1996.</p>"
                        ]
                    ),
                },
            ),
            (
                "Citation",
                _gen_extid(),
                {
                    "uri": set(["http://www.ica.org"]),
                },
            ),
            (
                "Convention",
                _gen_extid(),
                {
                    "convention_of": ["authorityrecord-FRAD033_EAC_00001"],
                    "description_format": set(["text/html"]),
                    "description": set(
                        [
                            '<p xmlns="urn:isbn:1-931666-33-4" '
                            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                            'xmlns:xlink="http://www.w3.org/1999/xlink">AFNOR '
                            "NF Z 44-060, octobre 1983, Catalogue "
                            "d\u2019auteurs et d\u2019anonymes : forme et\n          "
                            "structure des vedettes des collectivit\xe9s auteurs.</p>"
                        ]
                    ),
                },
            ),
            (
                "Convention",
                _gen_extid(),
                {
                    "convention_of": ["authorityrecord-FRAD033_EAC_00001"],
                    "description_format": set(["text/html"]),
                    "description": set(
                        [
                            '<p xmlns="urn:isbn:1-931666-33-4" '
                            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                            'xmlns:xlink="http://www.w3.org/1999/xlink">Norme ISO 8601 '
                            ":2004 \xc9l\xe9ments de donn\xe9es et formats "
                            "d\u2019\xe9change -- \xc9change\n          "
                            "d\u2019information -- Repr\xe9sentation de la date et "
                            "de l\u2019heure.</p>"
                        ]
                    ),
                },
            ),
            (
                "AgentKind",
                "agentkind/authority",
                {"name": set(["authority"])},
            ),
            (
                "NameEntry",
                _gen_extid(),
                {
                    "parts": set(["Gironde, Conseil général"]),
                    "form_variant": set(["authorized"]),
                    "name_entry_for": set(["authorityrecord-FRAD033_EAC_00001"]),
                },
            ),
            (
                "NameEntry",
                _gen_extid(),
                {
                    "parts": set(["CG33"]),
                    "form_variant": set(["alternative"]),
                    "name_entry_for": set(["authorityrecord-FRAD033_EAC_00001"]),
                },
            ),
            (
                "ParallelNames",
                _gen_extid(),
                {
                    "parallel_names_of": set(["authorityrecord-FRAD033_EAC_00001"]),
                    "simple_name_relation": set(["15", "14"]),
                    "authorized_form": set(["AFNOR_Z44-060\n\t"]),
                },
            ),
            (
                "NameEntry",
                _gen_extid(),
                {
                    "script_code": set(["Latn"]),
                    "preferred_form": ["AFNOR_Z44-060\n\t  "],
                    "parts": set(
                        ["Institut international des droits de\n\t  l'homme\n\t  "]
                    ),
                    "language": set(["fr"]),
                },
            ),
            (
                "NameEntry",
                _gen_extid(),
                {
                    "script_code": set(["Latn"]),
                    "parts": set(
                        ["International institute of human\n\t  rights\n\t  "]
                    ),
                    "language": set(["en"]),
                },
            ),
            (
                "ParallelNames",
                _gen_extid(),
                {
                    "parallel_names_of": set(["authorityrecord-FRAD033_EAC_00001"]),
                    "date_relation": set(["17", "18", "19"]),
                    "simple_name_relation": set(["20", "21", "22"]),
                },
            ),
            (
                "DateEntity",
                _gen_extid(),
                {"start_date": set([datetime.date(1949, 1, 1)])},
            ),
            (
                "DateEntity",
                _gen_extid(),
                {"start_date": set([datetime.date(1950, 1, 1)])},
            ),
            (
                "DateEntity",
                _gen_extid(),
                {"start_date": set([datetime.date(1950, 1, 1)])},
            ),
            (
                "NameEntry",
                _gen_extid(),
                {"parts": ["Federal Chancellery\n\t  of Germany\n\t  "]},
            ),
            (
                "NameEntry",
                _gen_extid(),
                {"parts": ["Chancellerie f\xe9d\xe9rale\n\t  d'Allemagne\n\t  "]},
            ),
            (
                "NameEntry",
                _gen_extid(),
                {"parts": set(["BK\n\t  "])},
            ),
            (
                "PostalAddress",
                _gen_extid(),
                {
                    "street": set(["1 Esplanade Charles de Gaulle"]),
                    "postalcode": set(["33074"]),
                    "raw_address": set(
                        ["1 Esplanade Charles de Gaulle\n33074\n Bordeaux Cedex"]
                    ),
                    "city": set([" Bordeaux Cedex"]),
                },
            ),
            (
                "AgentPlace",
                _gen_extid(),
                {
                    "role": set(["siege"]),
                    "place_agent": set(["authorityrecord-FRAD033_EAC_00001"]),
                    "place_entry_relation": set(["25"]),
                    "place_address": set(["23"]),
                },
            ),
            (
                "PlaceEntry",
                _gen_extid(),
                {
                    "name": set(["Bordeaux (Gironde, France)"]),
                    "equivalent_concept": set(
                        ["http://catalogue.bnf.fr/ark:/12148/cb152418385"]
                    ),
                },
            ),
            (
                "AgentPlace",
                _gen_extid(),
                {
                    "place_agent": set(["authorityrecord-FRAD033_EAC_00001"]),
                    "place_entry_relation": set(["27"]),
                    "role": set(["domicile"]),
                },
            ),
            (
                "PlaceEntry",
                _gen_extid(),
                {
                    "latitude": set(["43.60426"]),
                    "local_type": set(["other"]),
                    "longitude": set(["1.44367"]),
                    "name": set(["Toulouse (France)"]),
                },
            ),
            (
                "AgentPlace",
                _gen_extid(),
                {
                    "place_agent": set(["authorityrecord-FRAD033_EAC_00001"]),
                    "role": set(["dodo"]),
                    "place_entry_relation": set(["29"]),
                },
            ),
            (
                "PlaceEntry",
                _gen_extid(),
                {
                    "name": set(["Lit"]),
                },
            ),
            (
                "LegalStatus",
                _gen_extid(),
                {
                    "term": set(["Collectivité territoriale"]),
                    "date_relation": set(["31"]),
                    "description": set(["Description du statut"]),
                    "description_format": set(["text/plain"]),
                    "legal_status_agent": set(["authorityrecord-FRAD033_EAC_00001"]),
                },
            ),
            (
                "DateEntity",
                _gen_extid(),
                {
                    "start_date": set([datetime.date(1234, 1, 1)]),
                    "end_date": set([datetime.date(3000, 1, 1)]),
                },
            ),
            (
                "Mandate",
                _gen_extid(),
                {
                    "term": set(["1. Constitutions françaises"]),
                    "description": set(["Description du mandat"]),
                    "description_format": set(["text/plain"]),
                    "mandate_agent": set(["authorityrecord-FRAD033_EAC_00001"]),
                },
            ),
            (
                "History",
                _gen_extid(),
                {
                    "abstract": set(["Test of an abstract element"]),
                    "has_citation": set(["39", "40"]),
                    "has_event": set(["36", "34"]),
                    "text": set(
                        [
                            "\n".join(
                                (
                                    '<p xmlns="urn:isbn:1-931666-33-4" '
                                    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                                    'xmlns:xlink="http://www.w3.org/1999/xlink">{0}</p>'
                                ).format(text)
                                for text in [
                                    "La loi du 22 décembre 1789, en divisant ...",
                                    "L'inspecteur Canardo",
                                ]
                            )
                        ]
                    ),
                    "text_format": set(["text/html"]),
                    "items": set(
                        [
                            '<ul  >\n\t    <li>\n\t      <span style="font-'
                            '       style:italic">1450-1950\n\t      </span>\n\t'
                            "      (1929)\n\t    </li>\n\t    <li>\n\t      "
                            '<span style="font-style:italic">Globe\n\t      '
                            "Gliding\n\t      </span>\n\t      (1930)\n\t    </l"
                            'i>\n\t    <li>\n\t      <span style="font-     '
                            '  style:italic">Gems\n\t      </span>\n\t      '
                            "(1931)\n\t    </li>\n\t  </ul>\n      "
                        ]
                    ),
                    "items_format": set(["text/html"]),
                    "history_agent": set(["authorityrecord-FRAD033_EAC_00001"]),
                },
            ),
            (
                "HistoricalEvent",
                _gen_extid(),
                {
                    "date_relation": set(["35"]),
                    "event": [
                        "Left Mer and moved to the mainland.\n\t      "
                        "Worked at various jobs including canecutter\n\t      "
                        "and railway labourer.\n\t      "
                    ],
                },
            ),
            (
                "DateEntity",
                _gen_extid(),
                {
                    "end_date": [datetime.date(1957, 1, 1)],
                    "start_date": [datetime.date(1957, 1, 1)],
                },
            ),
            (
                "HistoricalEvent",
                _gen_extid(),
                {
                    "date_relation": set(["37"]),
                    "event": set(
                        [
                            "Union representative, Townsville-\n\t      "
                            "Mount Isa rail construction project.\n\t      "
                        ]
                    ),
                },
            ),
            (
                "DateEntity",
                _gen_extid(),
                {
                    "end_date": [datetime.date(1961, 1, 1)],
                    "start_date": [datetime.date(1960, 1, 1)],
                },
            ),
            (
                "Citation",
                _gen_extid(),
                {
                    "uri": set(
                        [
                            "http://www.assemblee-nationale.fr/histoire/images-decentralisation/"
                            "decentralisation/loi-du-22-decembre-1789-.pdf"
                        ]
                    )
                },
            ),
            (
                "Citation",
                _gen_extid(),
                {
                    "uri": set(["http://pifgadget"]),
                    "note": set(["Voir aussi pifgadget"]),
                },
            ),
            (
                "Structure",
                _gen_extid(),
                {
                    "description": set(
                        [
                            '<p xmlns="urn:isbn:1-931666-33-4" '
                            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                            'xmlns:xlink="http://www.w3.org/1999/xlink">Pour accomplir '
                            "ses missions ...</p>"
                        ]
                    ),
                    "description_format": set(["text/html"]),
                    "has_citation": set(["42"]),
                    "structure_agent": set(["authorityrecord-FRAD033_EAC_00001"]),
                },
            ),
            (
                "Citation",
                _gen_extid(),
                {
                    "note": set(
                        [
                            "L'\xe9l\xe9ment Citation \xe0 fournir un lien vers un document "
                            "externe comme un\n               organigramme ou un arbre "
                            "g\xe9n\xe9alogique. Pour une pr\xe9sentation plus simple, "
                            "sous forme\n               de texte, on peut utiliser un "
                            "ou plusieurs \xe9l\xe9m."
                        ]
                    )
                },
            ),
            (
                "AgentFunction",
                _gen_extid(),
                {
                    "description": set(
                        [
                            '<p xmlns="urn:isbn:1-931666-33-4" '
                            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                            'xmlns:xlink="http://www.w3.org/1999/xlink">Quatre grands '
                            "domaines de compétence...</p>"
                        ]
                    ),
                    "description_format": set(["text/html"]),
                    "function_agent": set(["authorityrecord-FRAD033_EAC_00001"]),
                },
            ),
            (
                "AgentFunction",
                _gen_extid(),
                {
                    "name": set(["action sociale"]),
                    "function_agent": set(["authorityrecord-FRAD033_EAC_00001"]),
                    "description": set(
                        [
                            '<p xmlns="urn:isbn:1-931666-33-4" '
                            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                            'xmlns:xlink="http://www.w3.org/1999/xlink">1. Solidarité\n'
                            "            blablabla.</p>"
                        ]
                    ),
                    "description_format": set(["text/html"]),
                    "equivalent_concept": set(
                        ["http://data.culture.fr/thesaurus/page/ark:/67717/T1-200"]
                    ),
                },
            ),
            (
                "AgentFunction",
                _gen_extid(),
                {
                    "name": set(["environnement"]),
                    "function_agent": set(["authorityrecord-FRAD033_EAC_00001"]),
                    "equivalent_concept": set(
                        ["http://data.culture.fr/thesaurus/page/ark:/67717/T1-1074"]
                    ),
                },
            ),
            (
                "Occupation",
                _gen_extid(),
                {
                    "term": set(["Réunioniste"]),
                    "date_relation": set(["47"]),
                    "description": set(["Organisation des réunions ..."]),
                    "description_format": set(["text/plain"]),
                    "occupation_agent": set(["authorityrecord-FRAD033_EAC_00001"]),
                    "has_citation": set(["48"]),
                    "equivalent_concept": set(["http://pifgadget.com"]),
                },
            ),
            (
                "DateEntity",
                _gen_extid(),
                {
                    "start_date": set([datetime.date(1987, 1, 1)]),
                    "end_date": set([datetime.date(2099, 1, 1)]),
                },
            ),
            (
                "Citation",
                _gen_extid(),
                {
                    "note": set(["la bible"]),
                },
            ),
            (
                "GeneralContext",
                _gen_extid(),
                {
                    "content": set(
                        [
                            '<p xmlns="urn:isbn:1-931666-33-4" '
                            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                            'xmlns:xlink="http://www.w3.org/1999/xlink">very famous</p>'
                        ]
                    ),
                    "content_format": set(["text/html"]),
                    "has_citation": set(["50"]),
                    "general_context_of": set(["authorityrecord-FRAD033_EAC_00001"]),
                },
            ),
            (
                "Citation",
                _gen_extid(),
                {
                    "note": set(["it's well known"]),
                },
            ),
            (
                "ExternalUri",
                "CG33-DIRADSJ",
                {
                    "uri": set(["CG33-DIRADSJ"]),
                    "cwuri": set(["CG33-DIRADSJ"]),
                },
            ),
            (
                "HierarchicalRelation",
                _gen_extid(),
                {
                    "entry": set(
                        [
                            "Gironde. Conseil général. Direction de l'administration et de "
                            "la sécurité juridique"
                        ]
                    ),
                    "date_relation": set(["52"]),
                    "description": set(["Coucou"]),
                    "description_format": set(["text/plain"]),
                    "hierarchical_parent": set(["CG33-DIRADSJ"]),
                    "hierarchical_child": set(["authorityrecord-FRAD033_EAC_00001"]),
                },
            ),
            (
                "DateEntity",
                _gen_extid(),
                {
                    "start_date": set([datetime.date(2008, 1, 1)]),
                    "end_date": set([datetime.date(2099, 1, 1)]),
                },
            ),
            (
                "ExternalUri",
                "whatever",
                {
                    "uri": set(["whatever"]),
                    "cwuri": set(["whatever"]),
                },
            ),
            (
                "ExternalUri",
                "/dev/null",
                {
                    "uri": set(["/dev/null"]),
                    "cwuri": set(["/dev/null"]),
                },
            ),
            (
                "ChronologicalRelation",
                _gen_extid(),
                {
                    "chronological_predecessor": set(["whatever"]),
                    "chronological_successor": set(
                        ["authorityrecord-FRAD033_EAC_00001"]
                    ),
                    "date_relation": set(["54"]),
                    "entry": set(["CG32"]),
                },
            ),
            (
                "DateEntity",
                _gen_extid(),
                {
                    "start_date": set([datetime.date(1917, 1, 1)]),
                    "end_date": set([datetime.date(2009, 1, 1)]),
                },
            ),
            (
                "ChronologicalRelation",
                _gen_extid(),
                {
                    "chronological_predecessor": set(
                        ["authorityrecord-FRAD033_EAC_00001"]
                    ),
                    "chronological_successor": set(["/dev/null"]),
                    "date_relation": set(["56"]),
                    "xml_wrap": set(
                        [
                            b'<gloups xmlns="urn:isbn:1-931666-33-4"'
                            b' xmlns:xsi="http://www.w3.org/2001/XML'
                            b'Schema-instance" xmlns:xlink="http://'
                            b'www.w3.org/1999/xlink">hips</gloups>'
                        ]
                    ),
                    "entry": set(["Trash"]),
                },
            ),
            (
                "DateEntity",
                _gen_extid(),
                {"start_date": set([datetime.date(2042, 1, 1)])},
            ),
            (
                "IdentityRelation",
                _gen_extid(),
                {
                    "date_relation": ["58"],
                    "entry": ["Trash"],
                    "identity_from": ["authorityrecord-FRAD033_EAC_00001"],
                    "identity_to": ["/dev/null"],
                    "xml_wrap": set(
                        [
                            b'<gloups xmlns="urn:isbn:1-931666-33-4" '
                            b'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                            b'xmlns:xlink="http://www.w3.org/1999/xlink">hips</gloups>'
                        ]
                    ),
                },
            ),
            ("DateEntity", _gen_extid(), {"start_date": [datetime.date(2042, 1, 1)]}),
            (
                "FamilyRelation",
                _gen_extid(),
                {
                    "date_relation": ["60"],
                    "entry": ["CG32"],
                    "family_from": ["authorityrecord-FRAD033_EAC_00001"],
                    "family_to": ["whatever"],
                },
            ),
            (
                "DateEntity",
                _gen_extid(),
                {
                    "end_date": [datetime.date(2009, 1, 1)],
                    "start_date": [datetime.date(1917, 1, 1)],
                },
            ),
            (
                "AssociationRelation",
                _gen_extid(),
                {
                    "association_from": set(["authorityrecord-FRAD033_EAC_00001"]),
                    "association_to": set(["agent-x"]),
                },
            ),
            (
                "EACResourceRelation",
                _gen_extid(),
                {
                    "agent_role": set(["creatorOf"]),
                    "date_relation": set(["63"]),
                    "xml_attributes": set(
                        [
                            '{"{http://www.w3.org/1999/xlink}actuate": "onRequest", '
                            '"{http://www.w3.org/1999/xlink}show": "new", '
                            '"{http://www.w3.org/1999/xlink}type": "simple"}'
                        ]
                    ),
                    "relation_entry": set(
                        [
                            "Gironde. Conseil g\xe9n\xe9ral. Direction de"
                            " l'administration et de la s\xe9curit\xe9 juridique"
                        ]
                    ),
                    "resource_role": set(["Fonds d'archives"]),
                    "resource_relation_resource": set(
                        ["http://gael.gironde.fr/ead.html?id=FRAD033_IR_N"]
                    ),
                    "resource_relation_agent": set(
                        ["authorityrecord-FRAD033_EAC_00001"]
                    ),
                    "xml_wrap": set(
                        [
                            b'<he xmlns="urn:isbn:1-931666-33-4" '
                            b'xmlns:xlink="http://www.w3.org/1999'
                            b'/xlink" xmlns:xsi="http://www.w3.org'
                            b'/2001/XMLSchema-instance">joe</he>'
                        ]
                    ),
                },
            ),
            (
                "DateEntity",
                _gen_extid(),
                {
                    "start_date": set([datetime.date(1673, 1, 1)]),
                    "end_date": set([datetime.date(1963, 1, 1)]),
                },
            ),
            (
                "EACFunctionRelation",
                _gen_extid(),
                {
                    "description": set(
                        [
                            '<p xmlns="urn:isbn:1-931666-33-4" xmlns:xsi="http:/'
                            '/www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http:'
                            '//www.w3.org/1999/xlink">The management of the University'
                            "'s\n\t  communication with its alumni.\n\t  </p>"
                        ]
                    ),
                    "r_type": set(["performs"]),
                    "description_format": set(["text/html"]),
                    "function_relation_agent": set(
                        ["authorityrecord-FRAD033_EAC_00001"]
                    ),
                    "function_relation_function": set(
                        ["http://gael.gironde.fr/ead.html?" "id=FRAD033_IR_N"]
                    ),
                    "relation_entry": set(
                        [
                            "Alumni communication\n\tmanagement, "
                            "University of\n\tGlasgow\n\t"
                        ]
                    ),
                    "xml_wrap": set(
                        [
                            b'<mods xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
                            b' xmlns="urn:isbn:1-931666-33-4" xmlns:xlink="http://www.w3'
                            b'.org/1999/xlink" xsi:schemaLocation="http://www.loc.gov'
                            b"/mods/v3 http:         //www.loc.gov/mods/v3/mods-3-3.xsd"
                            b'">\n\t    <titleInfo>\n\t      <title>Artisti trentini'
                            b" tra le due\n\t      guerre\n\t      </title>\n\t    </titleInfo"
                            b'>\n\t    <name>\n\t      <namePart type="given">Nicoletta'
                            b'\n\t      </namePart>\n\t      <namePart type="family'
                            b'">Boschiero\n\t      </namePart>\n\t      <role>\n\t\t<roleTerm'
                            b' type="text">autore\n\t\t</roleTerm>\n\t      </role>\n\t'
                            b"    </name>\n\t  </mods>\n\t"
                        ]
                    ),
                    "xml_attributes": set(
                        [
                            '{"{http://www.w3.org/1999/xlink}actuate": '
                            '"onLoad", "{http://www.w3.org/1999/xlink}arcrole": '
                            '"http://test_arcrole.lol.com", '
                            '"{http://www.w3.org/1999/xlink}role": '
                            '"http://test_role.lmao.com"}'
                        ]
                    ),
                },
            ),
            (
                "EACFunctionRelation",
                _gen_extid(),
                {
                    "function_relation_function": set(["FRAD033_IR_N"]),
                    "function_relation_agent": set(
                        ["authorityrecord-FRAD033_EAC_00001"]
                    ),
                    "description": set(
                        [
                            '<p xmlns="urn:isbn:1-931666-33-4" '
                            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                            'xmlns:xlink="http://www.w3.org/1999/xlink">'
                            "The second responsibility of the\n\t  "
                            "Department is to control the establishment\n\t  "
                            "and abolishment of schools.\n\t  </p>"
                        ]
                    ),
                    "r_type": set(["controls"]),
                    "description_format": set(["text/html"]),
                    "date_relation": set(["66"]),
                    "relation_entry": set(
                        ["Establishment and abolishment\n\tof schools\n\t"]
                    ),
                    "xml_attributes": set(["{}"]),
                },
            ),
            (
                "DateEntity",
                _gen_extid(),
                {
                    "start_date": set([datetime.date(1922, 1, 1)]),
                    "end_date": set([datetime.date(2001, 1, 1)]),
                },
            ),
            (
                "EACFunctionRelation",
                _gen_extid(),
                {
                    "function_relation_agent": set(
                        ["authorityrecord-FRAD033_EAC_00001"]
                    ),
                    "description": set(
                        [
                            '<p xmlns="urn:isbn:1-931666-33-4" '
                            'xmlns:xsi="http://www.w3.org/2001/X'
                            'MLSchema-instance" xmlns:xlink="http://ww'
                            'w.w3.org/1999/xlink">Some description'
                            "\n            </p>"
                        ]
                    ),
                    "function_relation_function": set(["ONLY_XLINK"]),
                    "description_format": set(["text/html"]),
                    "relation_entry": set(["Some relation entry\n          "]),
                    "xml_attributes": set(["{}"]),
                    "date_relation": ["68"],
                },
            ),
            (
                "DateEntity",
                _gen_extid(),
                {
                    "start_date": set([datetime.date(1922, 1, 1)]),
                    "end_date": set([datetime.date(2001, 1, 1)]),
                },
            ),
            (
                "EACFunctionRelation",
                _gen_extid(),
                {
                    "function_relation_agent": set(
                        ["authorityrecord-FRAD033_EAC_00001"]
                    ),
                    "description": set(
                        [
                            '<p xmlns="urn:isbn:1-931666-33-4" '
                            'xmlns:xsi="http://www.w3.org/2001/X'
                            'MLSchema-instance" xmlns:xlink="http://ww'
                            'w.w3.org/1999/xlink">Some description'
                            "\n            </p>"
                        ]
                    ),
                    "r_type": set(["ONLY_RELATION_TYPE"]),
                    "description_format": set(["text/html"]),
                    "relation_entry": set(["Some relation entry\n          "]),
                    "xml_attributes": set(["{}"]),
                    "date_relation": ["70"],
                },
            ),
            (
                "DateEntity",
                _gen_extid(),
                {
                    "start_date": set([datetime.date(1922, 1, 1)]),
                    "end_date": set([datetime.date(2001, 1, 1)]),
                },
            ),
            (
                "ExternalUri",
                "ONLY_XLINK",
                {"uri": set(["ONLY_XLINK"]), "cwuri": set(["ONLY_XLINK"])},
            ),
            (
                "ExternalUri",
                "FRAD033_IR_N",
                {"uri": set(["FRAD033_IR_N"]), "cwuri": set(["FRAD033_IR_N"])},
            ),
            (
                "ExternalUri",
                "http://gael.gironde.fr/ead.html?id=FRAD033_IR_N",
                {
                    "uri": set(["http://gael.gironde.fr/ead.html?id=FRAD033_IR_N"]),
                    "cwuri": set(["http://gael.gironde.fr/ead.html?id=FRAD033_IR_N"]),
                },
            ),
            (
                "ExternalUri",
                "agent-x",
                {"uri": set(["agent-x"]), "cwuri": set(["agent-x"])},
            ),
            (
                "ExternalUri",
                "http://data.culture.fr/thesaurus/page/ark:/67717/T1-200",
                {
                    "uri": set(
                        ["http://data.culture.fr/thesaurus/page/ark:/67717/T1-200"]
                    ),
                    "cwuri": set(
                        ["http://data.culture.fr/thesaurus/page/ark:/67717/T1-200"]
                    ),
                },
            ),
            (
                "ExternalUri",
                "http://data.culture.fr/thesaurus/page/ark:/67717/T1-1074",
                {
                    "uri": set(
                        ["http://data.culture.fr/thesaurus/page/ark:/67717/T1-1074"]
                    ),
                    "cwuri": set(
                        ["http://data.culture.fr/thesaurus/page/ark:/67717/T1-1074"]
                    ),
                },
            ),
            (
                "ExternalUri",
                "http://catalogue.bnf.fr/ark:/12148/cb152418385",
                {
                    "uri": set(["http://catalogue.bnf.fr/ark:/12148/cb152418385"]),
                    "cwuri": set(["http://catalogue.bnf.fr/ark:/12148/cb152418385"]),
                },
            ),
            (
                "ExternalUri",
                "http://pifgadget.com",
                {
                    "uri": set(["http://pifgadget.com"]),
                    "cwuri": set(["http://pifgadget.com"]),
                },
            ),
            (
                "AuthorityRecord",
                "authorityrecord-FRAD033_EAC_00001",
                {
                    "isni": set(["22330001300016"]),
                    "languages": ["English, Spanish"],
                    "start_date": set([datetime.date(1800, 1, 1)]),
                    "end_date": set([datetime.date(2099, 1, 1)]),
                    "agent_kind": set(["agentkind/authority"]),
                    "record_id": set(["FRAD033_EAC_00001"]),
                },
            ),
        ]
        expected = [ExtEntity(*vals) for vals in expected]
        fpath = self.datapath("FRAD033_EAC_00001_simplified.xml")
        import_log = SimpleImportLog(fpath)
        # Use a predictable extid_generator.
        extid_generator = map(str, count()).__next__
        importer = dataimport.EACCPFImporter(
            fpath, import_log, mock_, extid_generator=extid_generator
        )
        entities = list(importer.external_entities())
        # Used for an easier handling of the order error while generating the 2 lists
        self.check_order_entities(entities, expected)
        self.check_external_entities(entities, expected)
        visited = set([])
        for x in importer._visited.values():
            visited.update(x)
        self.assertCountEqual(visited, [x.extid for x in expected])
        # Gather not-visited tag by name and group source lines.
        not_visited = {}
        for tagname, sourceline in importer.not_visited():
            not_visited.setdefault(tagname, set([])).add(sourceline)
        self.assertEqual(
            not_visited,
            {
                "maintenanceStatus": set([12]),
                "publicationStatus": set([14]),
                "recordId": set([8]),
                "maintenanceAgency": set([16]),
                "languageDeclaration": set([21]),
                "languageUsed": set([188, 195]),
                "localControl": set([54]),
                "source": set([76]),  # empty.
                "structureOrGenealogy": set([268]),  # empty.
                "biogHist": set([328, 331]),  # empty.
            },
        )

    def check_order_entities(self, entities, expected):
        """Usefull test for comparing sorted lists of actual and
        expected entities. Make it easier to check where to add a
        new entity or swap 2 of them.
        """

        def get_sorted(elems):
            return sorted(
                ((e.etype, e.extid) for e in elems if e.etype != "ExternalUri"),
                key=lambda e: e[1],
            )

        a_lst = get_sorted(entities)
        e_lst = get_sorted(expected)
        self.assertEquals(a_lst, e_lst)

    def test_values_from_functions(self):
        fname = "FRAD033_EAC_00001_simplified.xml"
        fpath = self.datapath(fname)
        self.root = etree.fromstring(XML_TEST)
        import_log = SimpleImportLog(fpath)
        importer = dataimport.EACCPFImporter(fpath, import_log)
        values = importer.values_from_xpaths(
            self.root,
            (
                ("to_value", "to"),
                ("from_value", "from"),
                ("heading_value", "heading"),
                ("body_value", "body"),
                ("empty_value", "empty"),
            ),
        )
        self.assertEqual(
            values,
            {
                "to_value": set(["Tove"]),
                "from_value": set(["Jani"]),
                "heading_value": set(["Reminder"]),
                "body_value": set(["Hey!"]),
            },
        )
        attrib = importer.values_from_attrib(
            self.root, (("test_varname", "test"), ("test_varname_2", "test2"))
        )
        self.assertEqual(
            attrib,
            {
                "test_varname": set(["test_value"]),
                "test_varname_2": set(["test2_value"]),
            },
        )

    def test_mandate_under_mandates(self):
        """In FRAD033_EAC_00003.xml, <mandate> element are within <mandates>."""
        entities = list(self.file_extentities("FRAD033_EAC_00003.xml"))
        expected_terms = [
            "Code du patrimoine, Livre II",
            "Loi du 5 brumaire an V [26 octobre 1796]",
            (
                "Loi du 3 janvier 1979 sur les archives, accompagnée de ses décrets\n"
                "                        d’application datant du 3 décembre."
            ),
            "Loi sur les archives du 15 juillet 2008",
        ]
        self.assertCountEqual(
            [
                next(iter(x.values["term"]))
                for x in entities
                if x.etype == "Mandate" and "term" in x.values
            ],
            expected_terms,
        )
        mandate_with_link = next(
            x
            for x in entities
            if x.etype == "Mandate"
            and "Code du patrimoine, Livre II" in x.values["term"]
        )
        extid = next(iter(mandate_with_link.values["has_citation"]))
        url = (
            "http://www.legifrance.gouv.fr/affichCode.do?idArticle=LEGIARTI000019202816"
        )
        citation = next(
            x for x in entities if x.etype == "Citation" and url in x.values["uri"]
        )
        self.assertEqual(extid, citation.extid)

    def test_agentfunction_within_functions_tag(self):
        """In FRAD033_EAC_00003.xml, <function> element are within <functions>
        not <description>.
        """
        entities = self.file_extentities("FRAD033_EAC_00003.xml")
        self.assertCountEqual(
            [
                x.values["name"].pop()
                for x in entities
                if x.etype == "AgentFunction" and "name" in x.values
            ],
            ["contr\xf4le", "collecte", "classement", "restauration", "promotion"],
        )

    def test_no_nameentry_authorizedform(self):
        entities = self.file_extentities(
            "Service de l'administration generale et des assemblees.xml"
        )
        expected = (
            "Gironde. Conseil général. Service de l'administration "
            "générale et des assemblées"
        )
        self.assertIn(
            expected,
            [x.values["parts"].pop() for x in entities if x.etype == "NameEntry"],
        )

    def ctx_assert(self, method, actual, expected, ctx, msg=None):
        """Wrap assertion method with a context message"""
        try:
            getattr(self, method)(actual, expected, msg=msg)
        except AssertionError as exc:
            msg = str(exc)
            if ctx:
                msg = ("[%s] " % ctx) + msg
            raise AssertionError(msg)

    def check_external_entities(self, entities, expected):
        entities = extentities2dict(entities)
        expected = extentities2dict(expected)
        etypes, expected_etypes = list(entities), list(expected)
        self.ctx_assert("assertCountEqual", etypes, expected_etypes, ctx="etypes")

        def safe_int(value):
            try:
                return int(value)
            except ValueError:
                return 9999

        ordered_etypes = [
            x[1]
            for x in sorted(
                (min(safe_int(extid) for extid in edict), etype)
                for etype, edict in expected.items()
            )
        ]
        for etype in ordered_etypes:
            edict = expected[etype]
            entities_etype = entities[etype]
            extids, expected_extids = list(entities_etype), list(edict)
            self.ctx_assert(
                "assertCountEqual", extids, expected_extids, ctx="%s/extids" % etype
            )
            for extid, values in edict.items():
                self.ctx_assert(
                    "assertEqual",
                    tolist(entities_etype[extid]),
                    tolist(values),
                    ctx="%s/%s/values" % (etype, extid),
                )

    def test_errors(self):
        log = SimpleImportLog("<dummy>")
        with self.assertRaises(dataimport.InvalidXML):
            importer = dataimport.EACCPFImporter(BytesIO(b"no xml"), log, mock_)
            list(importer.external_entities())
        with self.assertRaises(dataimport.MissingTag):
            importer = dataimport.EACCPFImporter(BytesIO(b"<xml/>"), log, mock_)
            list(importer.external_entities())


class EACDataImportTC(CubicWebTC):
    def test_FRAD033_EAC_00001(self):
        fpath = self.datapath("FRAD033_EAC_00001_simplified.xml")
        with self.admin_access.repo_cnx() as cnx:
            self.maxDiff = None
            # create a skos concept to ensure it's used instead of a ExternalUri
            scheme = cnx.create_entity("ConceptScheme")
            scheme.add_concept(
                "environnement",
                cwuri="http://data.culture.fr/thesaurus/page/ark:/67717/T1-1074",
            )
            cnx.commit()
            created, updated = testutils.eac_import(cnx, fpath)
            self.assertEqual(len(created), 80)
            self.assertEqual(updated, set())
            rset = cnx.find("AuthorityRecord", isni="22330001300016")
            self.assertEqual(len(rset), 1)
            record = rset.one()
            self.assertEqual(record.kind, "authority")
            self.assertEqual(record.start_date, datetime.date(1800, 1, 1))
            self.assertEqual(record.end_date, datetime.date(2099, 1, 1))
            self.assertEqual(
                record.other_record_ids, [(None, "1234"), ("letters", "ABCD")]
            )
            address = record.postal_address[0]
            self.assertEqual(address.street, "1 Esplanade Charles de Gaulle")
            self.assertEqual(address.postalcode, "33074")
            self.assertEqual(address.city, " Bordeaux Cedex")
            self.assertEqual(
                address.raw_address,
                "1 Esplanade Charles de Gaulle\n33074\n Bordeaux Cedex",
            )
            rset = cnx.execute(
                """
                 Any R,N WHERE P place_agent A, A eid %(eid)s,
                 P role R, P place_entry_relation E, E name N""",
                {"eid": record.eid},
            )
            self.assertCountEqual(
                rset.rows,
                [
                    ["siege", "Bordeaux (Gironde, France)"],
                    ["domicile", "Toulouse (France)"],
                    ["dodo", "Lit"],
                ],
            )
            self.assertEqual(len(record.reverse_function_agent), 3)
            for related in (
                "structure",
                "history",
                "mandate",
                "occupation",
                "generalcontext",
                "legal_status",
                "eac_relations",
                "equivalent_concept",
                "control",
                "convention",
                "parallel_relations",
            ):
                with self.subTest(related=related):
                    checker = getattr(self, "_check_" + related)
                    checker(cnx, record)

    def _check_structure(self, cnx, record):
        rset = cnx.find("Structure", structure_agent=record)
        self.assertEqual(len(rset), 1)
        self.assertEqual(
            rset.one().printable_value("description", format="text/plain").strip(),
            "Pour accomplir ses missions ...",
        )

    def _check_convention(self, cnx, record):
        rset = cnx.find("Convention", convention_of=record).sorted_rset(lambda x: x.eid)
        self.assertEqual(len(rset), 3)
        self.assertEqual(
            rset.get_entity(0, 0)
            .printable_value("description", format="text/plain")
            .strip(),
            "Norme ISAAR(CPF) du Conseil international des archives, "
            "2e \xe9dition, 1996.",
        )

    def _check_history(self, cnx, record):
        rset = cnx.find("History", history_agent=record)
        self.assertEqual(len(rset), 1)
        entity = rset.one()
        self.assertEqual(
            entity.printable_value("abstract", format="text/plain").strip(),
            "Test of an abstract element",
        )
        self.assertEqual(
            entity.printable_value("text", format="text/plain").strip(),
            "La loi du 22 décembre 1789, en divisant ...\n\nL'inspecteur Canardo",
        )
        events = rset.one().has_event
        self.assertEqual(len(events), 2)

    def _check_mandate(self, cnx, record):
        rset = cnx.find("Mandate", mandate_agent=record)
        self.assertEqual(len(rset), 1)
        self.assertEqual(
            rset.one().printable_value("description", format="text/plain").strip(),
            "Description du mandat",
        )

    def _check_occupation(self, cnx, record):
        occupation = cnx.find("Occupation", occupation_agent=record).one()
        self.assertEqual(occupation.term, "Réunioniste")
        citation = occupation.has_citation[0]
        self.assertEqual(citation.note, "la bible")
        voc = occupation.equivalent_concept[0]
        self.assertEqual(voc.uri, "http://pifgadget.com")

    def _check_generalcontext(self, cnx, record):
        occupation = cnx.find("GeneralContext", general_context_of=record).one()
        self.assertIn("very famous", occupation.content)
        self.assertEqual(occupation.content_format, "text/html")
        citation = occupation.has_citation[0]
        self.assertEqual(citation.note, "it's well known")

    def _check_legal_status(self, cnx, record):
        rset = cnx.find("LegalStatus", legal_status_agent=record)
        self.assertEqual(len(rset), 1)
        self.assertEqual(
            rset.one().printable_value("description", format="text/plain").strip(),
            "Description du statut",
        )

    def _check_eac_relations(self, cnx, record):
        relation = cnx.find("HierarchicalRelation").one()
        self.assertEqual(
            relation.entry,
            "Gironde. Conseil général. Direction de "
            "l'administration et de la sécurité juridique",
        )
        self.assertEqual(
            relation.printable_value("description", format="text/plain"), "Coucou"
        )
        other_record = cnx.find("ExternalUri", uri="CG33-DIRADSJ").one()
        self.assertEqual(relation.hierarchical_parent[0], other_record)
        relation = cnx.find("AssociationRelation").one()
        self.assertEqual(relation.association_from[0], record)
        other_record = cnx.find("ExternalUri", uri="agent-x").one()
        self.assertEqual(other_record.cwuri, "agent-x")
        self.assertEqual(relation.association_to[0], other_record)
        rset = cnx.find("EACResourceRelation", agent_role="creatorOf")
        self.assertEqual(len(rset), 1)
        rrelation = rset.one()
        self.assertEqual(rrelation.resource_relation_agent[0], record)
        exturi = rrelation.resource_relation_resource[0]
        self.assertEqual(exturi.uri, "http://gael.gironde.fr/ead.html?id=FRAD033_IR_N")
        self.assertEqual(
            rrelation.xml_wrap.getvalue().decode(),
            '<he xmlns="urn:isbn:1-931666-33-4" xmlns:xlink="http'
            '://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org'
            '/2001/XMLSchema-instance">joe</he>',
        )
        self.assertEqual(
            rrelation.json_attrs,
            {
                "{http://www.w3.org/1999/xlink}actuate": "onRequest",
                "{http://www.w3.org/1999/xlink}show": "new",
                "{http://www.w3.org/1999/xlink}type": "simple",
            },
        )
        rset = cnx.find("EACFunctionRelation", r_type="performs")
        func_relation = rset.one()
        self.assertEqual(
            func_relation.json_attrs,
            {
                "{http://www.w3.org/1999/xlink}actuate": "onLoad",
                "{http://www.w3.org/1999/xlink}arcrole": "http://test_arcrole.lol.com",
                "{http://www.w3.org/1999/xlink}role": "http://test_role.lmao.com",
            },
        )
        self.assertEqual(
            func_relation.relation_entry,
            "Alumni communication\n\tmanagement, " "University of\n\tGlasgow\n\t",
        )
        self.assertEqual(
            func_relation.xml_wrap.getvalue().decode(),
            '<mods xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
            ' xmlns="urn:isbn:1-931666-33-4" xmlns:xlink="http://www.w3'
            '.org/1999/xlink" xsi:schemaLocation="http://www.loc.gov'
            "/mods/v3 http:         //www.loc.gov/mods/v3/mods-3-3.xsd"
            '">\n\t    <titleInfo>\n\t      <title>Artisti trentini tra'
            " le due\n\t      guerre\n\t      </title>\n\t    </titleInfo>\n"
            '\t    <name>\n\t      <namePart type="given">Nicoletta\n\t'
            '      </namePart>\n\t      <namePart type="family">Boschiero\n'
            '\t      </namePart>\n\t      <role>\n\t\t<roleTerm type="text'
            '">autore\n\t\t</roleTerm>\n\t      </role>\n\t    </name>\n\t'
            "  </mods>\n\t",
        )
        self.assertEqual(func_relation.function_relation_agent[0], record)
        self.assertEqual(
            func_relation.function_relation_function[0].uri,
            "http://gael.gironde.fr/ead.html?id=FRAD033_IR_N",
        )
        rset = cnx.find("EACFunctionRelation", r_type="controls")
        func_relation = rset.one()
        self.assertEqual(func_relation.function_relation_agent[0], record)
        self.assertEqual(
            func_relation.function_relation_function[0].uri, "FRAD033_IR_N"
        )

    def _check_parallel_relations(self, cnx, record):
        rset = cnx.find("ParallelNames", parallel_names_of=record).sorted_rset(
            lambda x: x.eid
        )
        self.assertEqual(len(rset), 2)
        p_entity = rset.get_entity(0, 0)
        self.assertEqual(p_entity.parallel_names_of[0], record)
        self.assertEqual(len(p_entity.simple_name_relation), 2)
        self.assertEqual(len(p_entity.date_relation), 0)
        p_entity = rset.get_entity(1, 0)
        self.assertEqual(p_entity.parallel_names_of[0], record)
        self.assertEqual(len(p_entity.simple_name_relation), 3)
        self.assertEqual(len(p_entity.date_relation), 3)

    def _check_equivalent_concept(self, cnx, record):
        functions = dict((f.name, f) for f in record.reverse_function_agent)
        self.assertEqual(
            functions["action sociale"].equivalent_concept[0].cwuri,
            "http://data.culture.fr/thesaurus/page/ark:/67717/T1-200",
        )
        self.assertEqual(
            functions["action sociale"].equivalent_concept[0].cw_etype, "ExternalUri"
        )
        self.assertEqual(
            functions["environnement"].equivalent_concept[0].cwuri,
            "http://data.culture.fr/thesaurus/page/ark:/67717/T1-1074",
        )
        self.assertEqual(
            functions["environnement"].equivalent_concept[0].cw_etype, "Concept"
        )
        self.assertEqual(
            functions["environnement"].vocabulary_source[0].eid,
            functions["environnement"].equivalent_concept[0].scheme.eid,
        )
        place = cnx.find("PlaceEntry", name="Bordeaux (Gironde, France)").one()
        self.assertEqual(
            place.equivalent_concept[0].cwuri,
            "http://catalogue.bnf.fr/ark:/12148/cb152418385",
        )

    def _check_control(self, cnx, record):
        rset = cnx.find("EACSource")
        self.assertEqual(len(rset), 2)
        rset = cnx.execute("Any A WHERE A generated X, X eid %(x)s", {"x": record.eid})
        self.assertEqual(len(rset), 2)
        rset = cnx.execute('Any A WHERE A agent "Delphine Jamet"')
        self.assertEqual(len(rset), 1)

    def test_multiple_imports(self):
        def count_entity(cnx, etype):
            return cnx.execute("Any COUNT(X) WHERE X is %s" % etype)[0][0]

        with self.admin_access.repo_cnx() as cnx:
            nb_records_before = count_entity(cnx, "AuthorityRecord")
            for fname in (
                "FRAD033_EAC_00001.xml",
                "FRAD033_EAC_00003.xml",
                "FRAD033_EAC_00071.xml",
            ):
                fpath = self.datapath(fname)
                created, updated = testutils.eac_import(cnx, fpath)
            nb_records_after = count_entity(cnx, "AuthorityRecord")
            self.assertEqual(nb_records_after - nb_records_before, 3)

    def test_unknown_kind(self):
        with self.admin_access.repo_cnx() as cnx:
            testutils.eac_import(cnx, self.datapath("custom_kind.xml"))
            self.assertRaises(
                NoResultError, cnx.find("AgentKind", name="a custom kind").one
            )
            self.assertEqual(
                cnx.find("AuthorityRecord").one().agent_kind[0].name,
                "unknown-agent-kind",
            )

    def test_no_name_entry(self):
        with self.admin_access.repo_cnx() as cnx:
            with self.assertRaises(dataimport.MissingTag) as cm:
                testutils.eac_import(cnx, self.datapath("no_name_entry.xml"))
            self.assertEqual(cm.exception.tag, "nameEntry")
            self.assertEqual(cm.exception.tag_parent, "identity")

    def test_no_name_entry_part(self):
        with self.admin_access.repo_cnx() as cnx:
            with self.assertRaises(dataimport.MissingTag) as cm:
                testutils.eac_import(cnx, self.datapath("no_name_entry_part.xml"))
            self.assertEqual(cm.exception.tag, "part")
            self.assertEqual(cm.exception.tag_parent, "nameEntry")


if __name__ == "__main__":
    unittest.main()
