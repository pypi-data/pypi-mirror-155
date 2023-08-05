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
"""cubicweb-eac test for views."""

import datetime
import unittest

from rdflib import ConjunctiveGraph, Graph
from rdflib.compare import graph_diff

from cubicweb.devtools import BASE_URL
from cubicweb.devtools.testlib import CubicWebTC

from cubicweb_eac import testutils

from utils import add_entity_to_graph


class AuthorityRecordRdfTC(CubicWebTC):
    def setup_database(self):
        with self.admin_access.cnx() as cnx:
            copain = testutils.authority_record(cnx, "B123", "Toto")
            copine = testutils.authority_record(cnx, "B234", "Titi")
            person = testutils.authority_record(
                cnx,
                "A123",
                "Jean Jacques",
                kind="person",
                start_date=datetime.date(2010, 1, 1),
                end_date=datetime.date(2050, 5, 2),
                reverse_occupation_agent=cnx.create_entity(
                    "Occupation", term="fan de poules"
                ),
                reverse_history_agent=cnx.create_entity(
                    "History", text="<p>loutre gentille<p>", text_format="text/html"
                ),
                reverse_family_from=(
                    cnx.create_entity("FamilyRelation", family_to=copain, entry="Toto"),
                    cnx.create_entity("FamilyRelation", family_to=copine, entry="Titi"),
                ),
            )
            parent_organization = testutils.authority_record(
                cnx, "P123", "Toto Cie", kind="authority"
            )
            child_organization = testutils.authority_record(
                cnx, "P243", "Titi Cie", kind="authority"
            )
            organization = testutils.authority_record(
                cnx,
                "C123",
                "Entreprise",
                kind="authority",
                start_date=datetime.date(2010, 1, 1),
                end_date=datetime.date(2050, 5, 2),
            )
            cnx.create_entity(
                "HierarchicalRelation",
                hierarchical_child=(child_organization),
                hierarchical_parent=(organization),
                entry="Titi Cie",
            )
            cnx.create_entity(
                "HierarchicalRelation",
                hierarchical_child=(organization),
                hierarchical_parent=(parent_organization),
                entry="Titi Cie",
            )
            fam1 = testutils.authority_record(
                cnx, "F123", "Famille Pigeon", kind="family"
            )
            fam2 = testutils.authority_record(
                cnx, "F234", "Famille Poulet", kind="family"
            )
            cnx.create_entity(
                "FamilyRelation",
                family_from=fam1,
                family_to=fam2,
                entry="Famille Poulet",
            )
            cnx.create_entity(
                "FamilyRelation",
                family_from=fam1,
                family_to=person,
                entry="Jean Jacques",
            )
            cnx.create_entity(
                "FamilyRelation",
                family_from=person,
                family_to=fam1,
                entry="Famille Poulet",
            )
            cnx.commit()

    def compare_graphs(self, graph, eid_dict, target_ttl_file_name):
        with open(self.datapath(target_ttl_file_name), "r") as f:
            data = f.read()
            data = data.replace("{{BASE_URL}}", BASE_URL)
            for key, value in eid_dict.items():
                data = data.replace("{{%s}}" % key, str(value))

            target_graph = Graph().parse(data=data, format="ttl")
            print(graph.serialize(format="ttl"))
            common, tested_only, target_only = graph_diff(graph, target_graph)
            print(target_only.serialize(format="ttl"))
            print(tested_only.serialize(format="ttl"))
            self.assertEqual(len(tested_only), 0)
            self.assertEqual(len(target_only), 0)

    def test_person_authority_schemaorg(self):
        with self.admin_access.repo_cnx() as cnx:
            entity = cnx.find("AuthorityRecord", record_id="A123").one()
            graph = ConjunctiveGraph()
            add_entity_to_graph(graph, entity, "rdf.schemaorg")
            self.compare_graphs(graph, {"eid": entity.eid}, "person_rdf.ttl")

    def test_organization_authority_schemaorg(self):
        with self.admin_access.repo_cnx() as cnx:
            entity = cnx.find("AuthorityRecord", record_id="C123").one()
            graph = ConjunctiveGraph()
            add_entity_to_graph(graph, entity, "rdf.schemaorg")
            self.compare_graphs(graph, {"eid": entity.eid}, "organization_rdf.ttl")

    def test_family_rico(self):
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute(
                "Any X, N, A WHERE X is AuthorityRecord, X record_id %(id)s,"
                "R is FamilyRelation, R family_from X,"
                "R family_to A, A agent_kind K, K name 'person',"
                "N name_entry_for X",
                {"id": "F123"},
            )
            eid, name, agent_person = rset[0]
            record = cnx.entity_from_eid(eid)

            rset = cnx.execute(
                "Any A WHERE X is AuthorityRecord, X record_id %(id)s,"
                "R is FamilyRelation, R family_from X,"
                "R family_to A, A agent_kind K, K name 'family'",
                {"id": "F123"},
            )
            family_eid = rset[0][0]
            graph = ConjunctiveGraph()
            add_entity_to_graph(graph, record, "rdf.rico")
            self.compare_graphs(
                graph,
                {
                    "eid": record.eid,
                    "p_eid": agent_person,
                    "name_eid": name,
                    "ar_eid": family_eid,
                },
                "family_rico.ttl",
            )

    def test_person_rico(self):
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute(
                "Any X, N, O WHERE X is AuthorityRecord, X record_id %(id)s,"
                "O occupation_agent X,"
                "N name_entry_for X",
                {"id": "A123"},
            )
            eid, name, occupation = rset[0]
            record = cnx.entity_from_eid(eid)

            rset = cnx.execute(
                "Any R, A WHERE X is AuthorityRecord, X record_id %(id)s,"
                "R is FamilyRelation, R family_from X,"
                "R family_to A, A agent_kind K, K name 'family'",
                {"id": "A123"},
            )
            rel_family, family_eid = rset[0]

            rset = cnx.execute(
                "Any A, R WHERE X is AuthorityRecord, X record_id %(id)s,"
                "R is FamilyRelation, R family_from X,"
                "R family_to A, A agent_kind K, K name 'person'",
                {"id": "A123"},
            )
            fam1, famrel1 = rset[0]
            fam2, famrel2 = rset[1]

            graph = ConjunctiveGraph()
            add_entity_to_graph(graph, record, "rdf.rico")
            self.compare_graphs(
                graph,
                {
                    "eid": eid,
                    "occupation": occupation,
                    "name": name,
                    "fam1": fam1,
                    "fam2": fam2,
                    "famrel1": famrel1,
                    "famrel2": famrel2,
                    "familyrel": rel_family,
                    "family": family_eid,
                },
                "person_rico.ttl",
            )

    def test_organization_rico(self):
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute(
                "Any X, N WHERE X is AuthorityRecord, X record_id %(id)s,"
                "N name_entry_for X",
                {"id": "C123"},
            )
            eid, name = rset[0]
            record = cnx.entity_from_eid(eid)

            rset = cnx.execute(
                "Any A, R WHERE X is AuthorityRecord, X record_id %(id)s,"
                "R is HierarchicalRelation, R hierarchical_child X,"
                "R hierarchical_parent A",
                {"id": "C123"},
            )
            child_of, child_of_rel = rset[0]

            rset = cnx.execute(
                "Any A, R WHERE X is AuthorityRecord, X record_id %(id)s,"
                "R is HierarchicalRelation, R hierarchical_parent X,"
                "R hierarchical_child A",
                {"id": "C123"},
            )
            parent_of, parent_of_rel = rset[0]

            graph = ConjunctiveGraph()
            add_entity_to_graph(graph, record, "rdf.rico")
            self.compare_graphs(
                graph,
                {
                    "eid": eid,
                    "name": name,
                    "parent_of": parent_of,
                    "parent_of_rel": parent_of_rel,
                    "child_of": child_of,
                    "child_of_rel": child_of_rel,
                },
                "organization_rico.ttl",
            )


if __name__ == "__main__":
    unittest.main()
