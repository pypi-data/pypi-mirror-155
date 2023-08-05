# coding: utf-8
# copyright 2021-2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

from rdflib import BNode, Literal, URIRef
from rdflib.term import _is_valid_uri

from logilab.common.decorators import cachedproperty

from cubicweb.predicates import is_instance
from cubicweb.entities.adapters import EntityRDFAdapter
from cubicweb.uilib import remove_html_tags


class AuthorityRecordRDFAdapter(EntityRDFAdapter):
    __regid__ = "rdf.schemaorg"
    __select__ = EntityRDFAdapter.__select__ & is_instance("AuthorityRecord")

    def names_triples(self):
        SCHEMA = self._use_namespace("schema")
        entity = self.entity
        for name_entry in entity.reverse_name_entry_for:
            if name_entry.parts:
                yield (self.uri, SCHEMA.name, Literal(name_entry.parts))

    def person_triples(self):
        SCHEMA = self._use_namespace("schema")
        RDF = self._use_namespace("rdf")
        entity = self.entity
        yield (self.uri, RDF.type, SCHEMA.Person)
        if entity.start_date:
            yield (
                self.uri,
                SCHEMA.birthDate,
                Literal(entity.start_date.strftime("%Y-%m-%d")),
            )
        if entity.end_date:
            yield (
                self.uri,
                SCHEMA.deathDate,
                Literal(entity.end_date.strftime("%Y-%m-%d")),
            )
        if entity.reverse_occupation_agent:
            yield (
                self.uri,
                SCHEMA.hasOccupation,
                Literal(entity.reverse_occupation_agent[0].term),
            )
        if entity.reverse_history_agent:
            yield (
                self.uri,
                SCHEMA.description,
                Literal(remove_html_tags(entity.reverse_history_agent[0].text)),
            )
        for family_member in entity.reverse_family_from:
            yield (self.uri, SCHEMA.relatedTo, Literal(family_member.entry))

    def organization_triples(self):
        SCHEMA = self._use_namespace("schema")
        RDF = self._use_namespace("rdf")
        entity = self.entity
        yield (self.uri, RDF.type, SCHEMA.Organization)
        if entity.start_date:
            yield (
                self.uri,
                SCHEMA.foundingDate,
                Literal(entity.start_date.strftime("%Y-%m-%d")),
            )
        if entity.end_date:
            yield (
                self.uri,
                SCHEMA.dissolutionDate,
                Literal(entity.end_date.strftime("%Y-%m-%d")),
            )

        for parent_of_relation in entity.reverse_hierarchical_parent:
            yield (
                self.uri,
                SCHEMA.subOrganization,
                Literal(parent_of_relation.hierarchical_child[0].dc_title()),
            )

        for child_of_relation in entity.reverse_hierarchical_child:
            yield (
                self.uri,
                SCHEMA.parentOrganization,
                Literal(child_of_relation.hierarchical_parent[0].dc_title()),
            )

    def triples(self):
        SCHEMA = self._use_namespace("schema")
        entity = self.entity
        yield (self.uri, SCHEMA.url, Literal(self.uri))
        yield from self.names_triples()

        for identity_relation in entity.reverse_identity_from:
            same_as_entity = identity_relation.identity_to[0]
            if same_as_entity.cw_etype == "ExternalUri":
                yield (self.uri, SCHEMA.sameAs, Literal(same_as_entity.uri))
            else:
                same_as_uri = same_as_entity.cw_adapt_to("rdf").uri
                yield (self.uri, SCHEMA.sameAs, Literal(same_as_uri))
        if entity.agent_kind:
            if entity.agent_kind[0].name == "person":
                yield from self.person_triples()
            else:
                yield from self.organization_triples()


def directional_relation_uri(relation_type, source_record, target_record):
    return URIRef(
        f"{source_record.cw_adapt_to('rdf').uri}#{relation_type}_to_{target_record.record_id}"
    )


def symmetric_relation_uri(relation_type, record_a, record_b):
    records = sorted([record_a, record_b], key=lambda x: x.record_id)
    return URIRef(
        f"{records[0].cw_adapt_to('rdf').uri}#{relation_type}_to_{records[1].record_id}"
    )


class AuthorityRecordRICORDFAdapter(EntityRDFAdapter):
    __regid__ = "rdf.rico"
    __select__ = EntityRDFAdapter.__select__ & is_instance("AuthorityRecord")

    @cachedproperty
    def agent_uri(self):
        return URIRef(f"{self.uri}#agent")

    @cachedproperty
    def inst_uri(self):
        return URIRef(f"{self.uri}#inst")

    def relation_triples(
        self,
        class_uri,
        relation_uri,
        source_uri,
        target_uri,
        prop_source,
        prop_source_inverse,
        prop_target,
        prop_target_inverse,
        reduced_prop,
        reduced_prop_inverse,
        desc=None,
        start=None,
        end=None,
    ):
        RDF = self._use_namespace("rdf")
        RICO = self._use_namespace(
            "rico", base_url="https://www.ica.org/standards/RiC/ontology#"
        )
        yield (relation_uri, RDF.type, class_uri)
        yield (relation_uri, prop_source, source_uri)
        yield (relation_uri, prop_target, target_uri)
        yield (source_uri, prop_source_inverse, relation_uri)
        yield (target_uri, prop_target_inverse, relation_uri)
        yield (source_uri, reduced_prop, target_uri)
        yield (target_uri, reduced_prop_inverse, source_uri)
        if start:
            yield (relation_uri, RICO.beginningDate, Literal(start))
        if end:
            yield (relation_uri, RICO.endDate, Literal(end))
        if desc:
            yield (relation_uri, RICO.descriptiveNote, Literal(remove_html_tags(desc)))

    def person_triples(self):
        RICO = self._use_namespace(
            "rico", base_url="https://www.ica.org/standards/RiC/ontology#"
        )
        if self.entity.start_date:
            yield (self.agent_uri, RICO.birthDate, Literal(self.entity.start_date))
        if self.entity.end_date:
            yield (self.agent_uri, RICO.deathDate, Literal(self.entity.end_date))
        family_relations = self._cw.execute(
            "Any AGENT, KIND, DESC WHERE "
            "F is FamilyRelation, F family_from X,"
            "F family_to AGENT, AGENT agent_kind K, K name KIND,"
            "AGENT is AuthorityRecord, F description DESC,"
            "X is AuthorityRecord, X eid %(eid)s",
            {"eid": self.entity.eid},
        )
        if family_relations:
            for agent_eid, kind, desc in family_relations:
                fam_agent_record = self._cw.entity_from_eid(agent_eid)
                relation_uri = symmetric_relation_uri(
                    "family", fam_agent_record, self.entity
                )

                fam_agent_uri = fam_agent_record.cw_adapt_to(self.__regid__).agent_uri

                if kind == "person":
                    yield from self.relation_triples(
                        RICO.FamilyRelation,
                        relation_uri,
                        self.agent_uri,
                        fam_agent_uri,
                        RICO.familyRelationConnects,
                        RICO.personHasFamilyRelation,
                        RICO.familyRelationConnects,
                        RICO.personHasFamilyRelation,
                        RICO.hasFamilyAssociationWith,
                        RICO.hasFamilyAssociationWith,
                        desc=desc,
                    )
                else:
                    yield from self.relation_triples(
                        RICO.MembershipRelation,
                        relation_uri,
                        fam_agent_uri,
                        self.agent_uri,
                        RICO.membershipRelationHasSource,
                        RICO.groupIsSourceOfMembershipRelation,
                        RICO.membershipRelationHasTarget,
                        RICO.personIsTargetOfMembershipRelation,
                        RICO.hasOrHadMember,
                        RICO.isOrWasMemberOf,
                        desc=desc,
                    )

    def family_triples(self):
        RICO = self._use_namespace(
            "rico", base_url="https://www.ica.org/standards/RiC/ontology#"
        )
        if self.entity.start_date:
            yield (self.agent_uri, RICO.beginningDate, Literal(self.entity.start_date))
        if self.entity.end_date:
            yield (self.agent_uri, RICO.endDate, Literal(self.entity.end_date))

        family_relations = self._cw.execute(
            "Any F, AGENT, KIND, DESC WHERE "
            "F is FamilyRelation, F family_from X,"
            "F family_to AGENT, AGENT agent_kind K, K name KIND,"
            "AGENT is AuthorityRecord, F description DESC,"
            "X is AuthorityRecord, X eid %(eid)s",
            {"eid": self.entity.eid},
        )
        if family_relations:
            for rel_eid, agent_eid, kind, desc in family_relations:
                fam_agent_record = self._cw.entity_from_eid(agent_eid)
                relation_uri = symmetric_relation_uri(
                    "family", fam_agent_record, self.entity
                )

                fam_agent_uri = fam_agent_record.cw_adapt_to(self.__regid__).agent_uri
                if kind == "person":
                    yield from self.relation_triples(
                        RICO.MembershipRelation,
                        relation_uri,
                        self.agent_uri,
                        fam_agent_uri,
                        RICO.membershipRelationHasSource,
                        RICO.groupIsSourceOfMembershipRelation,
                        RICO.membershipRelationHasTarget,
                        RICO.personIsTargetOfMembershipRelation,
                        RICO.hasOrHadMember,
                        RICO.isOrWasMemberOf,
                        desc=desc,
                    )
                else:
                    yield from self.relation_triples(
                        RICO.AgentToAgentRelation,
                        relation_uri,
                        self.agent_uri,
                        fam_agent_uri,
                        RICO.agentRelationConnects,
                        RICO.agentIsConnectedToAgentRelation,
                        RICO.agentRelationConnects,
                        RICO.agentIsConnectedToAgentRelation,
                        RICO.isAgentAssociatedWithAgent,
                        RICO.isAgentAssociatedWithAgent,
                    )

    def hierarchical_triples(
        self, relation_uri, parent_uri, child_uri, desc, start, end
    ):
        RICO = self._use_namespace(
            "rico", base_url="https://www.ica.org/standards/RiC/ontology#"
        )
        yield from self.relation_triples(
            RICO.AgentHierarchicalRelation,
            relation_uri,
            parent_uri,
            child_uri,
            RICO.agentHierarchicalRelationHasSource,
            RICO.agentIsSourceOfAgentHierarchicalRelation,
            RICO.agentHierarchicalRelationHasTarget,
            RICO.agentIsTargetOfAgentHierarchicalRelation,
            RICO.hasOrHadSubordinate,
            RICO.isOrWasSubordinateTo,
            desc,
            start,
            end,
        )

    def successor_triples(
        self, relation_uri, predecessor_uri, successor_uri, desc, start
    ):
        RICO = self._use_namespace(
            "rico", base_url="https://www.ica.org/standards/RiC/ontology#"
        )
        yield from self.relation_triples(
            RICO.AgentTemporalRelation,
            relation_uri,
            predecessor_uri,
            successor_uri,
            RICO.agentTemporalRelationHasSource,
            RICO.agentIsSourceOfAgentTemporalRelation,
            RICO.agentTemporalRelationHasTarget,
            RICO.agentIsTargetOfAgentTemporalRelation,
            RICO.hasSuccessor,
            RICO.isSuccessorOf,
            desc=desc,
        )
        if start:
            yield (relation_uri, RICO.date, Literal(start))

    def authority_triples(self):
        RICO = self._use_namespace(
            "rico", base_url="https://www.ica.org/standards/RiC/ontology#"
        )
        if self.entity.start_date:
            yield (
                self.agent_uri,
                RICO.beginningDate,
                Literal(self.entity.start_date),
            )
        if self.entity.end_date:
            yield (self.agent_uri, RICO.endDate, Literal(self.entity.end_date))

        sub_organizations = self._cw.execute(
            "Any AGENT, DESC, START, END WHERE "
            "R is HierarchicalRelation, R hierarchical_parent X,"
            "R hierarchical_child AGENT,"
            "AGENT is AuthorityRecord, R description DESC,"
            "X is AuthorityRecord, X eid %(eid)s,"
            "R date_relation D?, D is DateEntity,"
            "D start_date START?, D end_date END?",
            {"eid": self.entity.eid},
        )
        if sub_organizations:
            for agent_eid, desc, start, end in sub_organizations:
                child_authority_record = self._cw.entity_from_eid(agent_eid)
                relation_uri = directional_relation_uri(
                    "hierarchical", self.entity, child_authority_record
                )

                child_uri = child_authority_record.cw_adapt_to(self.__regid__).agent_uri

                yield from self.hierarchical_triples(
                    relation_uri, self.agent_uri, child_uri, desc, start, end
                )
        super_organizations = self._cw.execute(
            "Any AGENT, DESC, START, END WHERE "
            "R is HierarchicalRelation, R hierarchical_child X,"
            "R hierarchical_parent AGENT,"
            "AGENT is AuthorityRecord, R description DESC,"
            "X is AuthorityRecord, X eid %(eid)s,"
            "R date_relation D?, D is DateEntity,"
            "D start_date START?, D end_date END?",
            {"eid": self.entity.eid},
        )
        if super_organizations:
            for agent_eid, desc, start, end in super_organizations:
                parent_authority_record = self._cw.entity_from_eid(agent_eid)
                relation_uri = directional_relation_uri(
                    "hierarchical", parent_authority_record, self.entity
                )

                parent_uri = parent_authority_record.cw_adapt_to(
                    self.__regid__
                ).agent_uri

                yield from self.hierarchical_triples(
                    relation_uri, parent_uri, self.agent_uri, desc, start, end
                )

    def agent_triples(self):
        RICO = self._use_namespace(
            "rico", base_url="https://www.ica.org/standards/RiC/ontology#"
        )
        RDF = self._use_namespace("rdf")
        RDFS = self._use_namespace("rdfs")
        OWL = self._use_namespace("owl")

        KIND_TO_URI = {
            "person": RICO.Person,
            "authority": RICO.CorporateBody,
            "family": RICO.Family,
        }

        yield (self.agent_uri, RDF.type, RICO.Agent)
        agent_kind = self.entity.agent_kind[0].name
        if agent_kind in KIND_TO_URI:
            yield (
                self.agent_uri,
                RDF.type,
                KIND_TO_URI[self.entity.agent_kind[0].name],
            )

        if agent_kind == "person":
            yield from self.person_triples()
        elif agent_kind == "family":
            yield from self.family_triples()
        else:
            yield from self.authority_triples()

        association_relations = self._cw.execute(
            "Any R, AGENT, DESC, START, END WHERE "
            "R is AssociationRelation, R association_from X,"
            "R association_to AGENT, R description DESC,"
            "AGENT is AuthorityRecord,"
            "X is AuthorityRecord, X eid %(eid)s,"
            "R date_relation D?, D is DateEntity,"
            "D start_date START?, D end_date END?",
            {"eid": self.entity.eid},
        )
        if association_relations:
            for rel_eid, agent_eid, desc, start, end in association_relations:
                associated_agent_record = self._cw.entity_from_eid(agent_eid)
                relation_uri = symmetric_relation_uri(
                    "association", associated_agent_record, self.entity
                )

                rel_agent_uri = associated_agent_record.cw_adapt_to(
                    self.__regid__
                ).agent_uri
                yield from self.relation_triples(
                    RICO.AgentToAgentRelation,
                    relation_uri,
                    self.agent_uri,
                    rel_agent_uri,
                    RICO.agentRelationConnects,
                    RICO.agentIsConnectedToAgentRelation,
                    RICO.agentRelationConnects,
                    RICO.agentIsConnectedToAgentRelation,
                    RICO.isAgentAssociatedWithAgent,
                    RICO.isAgentAssociatedWithAgent,
                    desc,
                    start,
                    end,
                )

        predecessors = self._cw.execute(
            "Any AGENT, DESC, START WHERE "
            "R is ChronologicalRelation, R chronological_successor X,"
            "R chronological_predecessor AGENT, R description DESC,"
            "AGENT is AuthorityRecord,"
            "X is AuthorityRecord, X eid %(eid)s,"
            "R date_relation D?, D is DateEntity,"
            "D start_date START?",
            {"eid": self.entity.eid},
        )
        if predecessors:
            for agent_eid, desc, start in predecessors:
                predecessor_authority_record = self._cw.entity_from_eid(agent_eid)
                relation_uri = directional_relation_uri(
                    "temporal", predecessor_authority_record, self.entity
                )

                predecessor_uri = predecessor_authority_record.cw_adapt_to(
                    self.__regid__
                ).agent_uri

                yield from self.successor_triples(
                    relation_uri, predecessor_uri, self.agent_uri, desc, start
                )

        successors = self._cw.execute(
            "Any AGENT, DESC, START WHERE "
            "R is ChronologicalRelation, R chronological_predecessor X,"
            "R chronological_successor AGENT, R description DESC,"
            "AGENT is AuthorityRecord,"
            "X is AuthorityRecord, X eid %(eid)s,"
            "R date_relation D?, D is DateEntity,"
            "D start_date START?",
            {"eid": self.entity.eid},
        )
        if successors:
            for agent_eid, desc, start in successors:
                successor_authority_record = self._cw.entity_from_eid(agent_eid)
                relation_uri = directional_relation_uri(
                    "temporal", self.entity, successor_authority_record
                )

                successor_uri = successor_authority_record.cw_adapt_to(
                    self.__regid__
                ).agent_uri

                yield from self.successor_triples(
                    relation_uri, self.agent_uri, successor_uri, desc, start
                )

        yield (self.agent_uri, RICO.isOrWasDescribedBy, self.uri)
        function_rset = self._cw.execute(
            "Any F, NAME, START, END WHERE "
            "F is AgentFunction, F function_agent X,"
            "X is AuthorityRecord, X eid %(eid)s,"
            "F name NAME,"
            "F date_relation D?, D is DateEntity,"
            "D start_date START?, D end_date END?",
            {"eid": self.entity.eid},
        )

        if function_rset:
            for func_eid, func_name, start, end in function_rset:
                perf_uri = BNode()
                activity_uri = BNode()
                activity_type_uri = (
                    self._cw.entity_from_eid(func_eid).cw_adapt_to("rdf").uri
                )

                yield from self.relation_triples(
                    RICO.PerformanceRelation,
                    perf_uri,
                    activity_uri,
                    self.agent_uri,
                    RICO.performanceRelationHasSource,
                    RICO.activityIsSourceOfPerformanceRelation,
                    RICO.performanceRelationHasTarget,
                    RICO.agentIsTargetOfPerformanceRelation,
                    RICO.isOrWasPerformedBy,
                    RICO.performsOrPerformed,
                    None,
                    start,
                    end,
                )

                yield (activity_uri, RICO.hasActivityType, activity_type_uri)
                yield (activity_uri, RDF.type, RICO.Activity)
                yield (activity_type_uri, RDF.type, RICO.ActivityType)
                yield (activity_type_uri, RDFS.label, Literal(func_name))

        occupation_rset = self._cw.execute(
            "Any O, NAME, START, END WHERE "
            "O is Occupation, O occupation_agent X,"
            "X is AuthorityRecord, X eid %(eid)s,"
            "O term NAME,"
            "O date_relation D?, D is DateEntity,"
            "D start_date START?, D end_date END?",
            {"eid": self.entity.eid},
        )

        if occupation_rset:
            for occ_eid, occ_name, start, end in occupation_rset:
                perf_uri = BNode()
                occupation_uri = BNode()
                occupation_type_uri = (
                    self._cw.entity_from_eid(occ_eid).cw_adapt_to("rdf").uri
                )

                yield from self.relation_triples(
                    RICO.PerformanceRelation,
                    perf_uri,
                    occupation_uri,
                    self.agent_uri,
                    RICO.performanceRelationHasSource,
                    RICO.activityIsSourceOfPerformanceRelation,
                    RICO.performanceRelationHasTarget,
                    RICO.agentIsTargetOfPerformanceRelation,
                    RICO.isOrWasPerformedBy,
                    RICO.performsOrPerformed,
                    None,
                    start,
                    end,
                )
                yield (occupation_uri, RDF.type, RICO.Activity)
                yield (occupation_uri, RICO.hasActivityType, occupation_type_uri)
                yield (occupation_type_uri, RDF.type, RICO.OccupationType)
                yield (occupation_type_uri, RDFS.label, Literal(occ_name))

                yield (
                    self.agent_uri,
                    RICO.hasOrHadOccupationOfType,
                    occupation_type_uri,
                )
                yield (
                    occupation_type_uri,
                    RICO.isOrWasOccupationTypeOf,
                    self.agent_uri,
                )

        legal_status_rset = self._cw.execute(
            "Any S, NAME, START, END WHERE "
            "S is LegalStatus, S legal_status_agent X,"
            "X is AuthorityRecord, X eid %(eid)s,"
            "S term NAME,"
            "S date_relation D?, D is DateEntity,"
            "D start_date START?, D end_date END?",
            {"eid": self.entity.eid},
        )

        if legal_status_rset:
            for stat_eid, stat_name, start, end in legal_status_rset:
                relation_uri = BNode()
                legal_status_uri = (
                    self._cw.entity_from_eid(stat_eid).cw_adapt_to("rdf").uri
                )

                yield from self.relation_triples(
                    RICO.TypeRelation,
                    relation_uri,
                    legal_status_uri,
                    self.agent_uri,
                    RICO.typeRelationHasSource,
                    RICO.typeIsSourceOfTypeRelation,
                    RICO.typeRelationHasTarget,
                    RICO.thingIsTargetOfTypeRelation,
                    RICO.isOrWasLegalStatusOf,
                    RICO.hasOrHadLegalStatus,
                    None,
                    start,
                    end,
                )
                yield (legal_status_uri, RDF.type, RICO.LegalStatus)
                yield (legal_status_uri, RDFS.label, Literal(stat_name))

        mandate_rset = self._cw.execute(
            "Any M, NAME, DESC, START, END, NOTE, URL WHERE "
            "M is Mandate, M mandate_agent X,"
            "X is AuthorityRecord, X eid %(eid)s,"
            "M term NAME, M description DESC,"
            "M date_relation D?, D is DateEntity,"
            "D start_date START?, D end_date END?,"
            "M has_citation C?, C note NOTE?, C uri URL?",
            {"eid": self.entity.eid},
        )

        if mandate_rset:
            for (
                mand_eid,
                mand_name,
                mand_desc,
                start,
                end,
                note,
                mand_url,
            ) in mandate_rset:
                relation_uri = BNode()
                mandate_uri = self._cw.entity_from_eid(mand_eid).cw_adapt_to("rdf").uri

                yield from self.relation_triples(
                    RICO.MandateRelation,
                    relation_uri,
                    mandate_uri,
                    self.agent_uri,
                    RICO.mandateRelationHasSource,
                    RICO.mandateIsSourceOfMandateRelation,
                    RICO.mandateRelationHasTarget,
                    RICO.agentIsTargetOfMandateRelation,
                    RICO.authorizes,
                    RICO.authorizedBy,
                    mand_desc,
                    start,
                    end,
                )
                yield (mandate_uri, RDF.type, RICO.Mandate)
                if mand_name or note:
                    yield (
                        mandate_uri,
                        RDFS.label,
                        Literal(
                            f"{' -- '.join([x for x in (mand_name, note) if x is not None])}"
                        ),
                    )
                if mand_url:
                    yield (mandate_uri, RDFS.seeAlso, Literal(mand_url))

        place_entries = self._cw.execute(
            "Any P, PE, NAME, ROLE, LAT, LONG, START, END WHERE "
            "P is AgentPlace, P place_agent X,"
            "P role ROLE,"
            "X is AuthorityRecord, X eid %(eid)s,"
            "P place_entry_relation PE, PE is PlaceEntry,"
            "PE latitude LAT, PE longitude LONG,"
            "PE name NAME,"
            "P date_relation D?, D is DateEntity,"
            "D start_date START?, D end_date END?",
            {"eid": self.entity.eid},
        )

        if place_entries:
            for (
                rel_eid,
                place_eid,
                name,
                role,
                latitude,
                longitude,
                start,
                end,
            ) in place_entries:
                relation_uri = self._cw.entity_from_eid(rel_eid).cw_adapt_to("rdf").uri

                place_uri = self._cw.entity_from_eid(place_eid).cw_adapt_to("rdf").uri

                yield from self.relation_triples(
                    RICO.PlaceRelation,
                    relation_uri,
                    place_uri,
                    self.agent_uri,
                    RICO.placeRelationHasSource,
                    RICO.placeIsSourceOfPlaceRelation,
                    RICO.placeRelationHasTarget,
                    RICO.thingIsTargetOfPlaceRelation,
                    RICO.isOrWasLocationOf,
                    RICO.hasOrHadLocation,
                    None,
                    start,
                    end,
                )
                yield (relation_uri, RICO.type, Literal(role))
                yield (place_uri, RDF.type, RICO.Place)
                yield (place_uri, RICO.location, Literal(name))

                if latitude and longitude:
                    yield (
                        place_uri,
                        RICO.geographicalCoordinates,
                        Literal(f"{latitude} {longitude}"),
                    )

        name_entries = self._cw.execute(
            "Any N, NAME, TYPE, START, END WHERE "
            "N is NameEntry, N name_entry_for X,"
            "X is AuthorityRecord, X eid %(eid)s,"
            "N parts NAME, N form_variant TYPE,"
            "N date_relation D?, D is DateEntity,"
            "D start_date START?, D end_date END?",
            {"eid": self.entity.eid},
        )

        if name_entries:
            for (name_eid, name, variant, start, end) in name_entries:
                relation_uri = BNode()
                name_uri = self._cw.entity_from_eid(name_eid).cw_adapt_to("rdf").uri

                yield (self.agent_uri, RICO.name, Literal(name))
                yield (self.agent_uri, RICO.hasOrHadAgentName, name_uri)
                yield (name_uri, RICO.isOrWasAgentNameOf, self.agent_uri)
                yield (name_uri, RDF.type, RICO.AgentName)
                yield (name_uri, RICO.textualValue, Literal(name))
                if variant:
                    yield (name_uri, RICO.type, Literal(variant))
                if start:
                    yield (name_uri, RICO.usedFromDate, Literal(start))
                if end:
                    yield (name_uri, RICO.usedToDate, Literal(end))

        same_as = self._cw.execute(
            "Any URI WHERE "
            "R is IdentityRelation, R identity_from X,"
            "X is AuthorityRecord, X eid %(eid)s,"
            "R identity_to E, E is ExternalUri,"
            "E cwuri URI",
            {"eid": self.entity.eid},
        )

        if same_as:
            for uris in same_as:
                same_as_uri = uris[0]
                if _is_valid_uri(same_as_uri):
                    yield (self.agent_uri, OWL.sameAs, URIRef(same_as_uri))

    def record_triples(self):
        RICO = self._use_namespace(
            "rico", base_url="https://www.ica.org/standards/RiC/ontology#"
        )
        RDF = self._use_namespace("rdf")
        RICO_FORM = self._use_namespace(
            "ricoform",
            base_url="https://www.ica.org/standards/RiC/vocabularies/documentaryFormTypes#",
        )
        yield (self.inst_uri, RDF.type, RICO.Instantiation)
        yield (self.inst_uri, RICO.isInstantiationOf, self.uri)
        yield (self.inst_uri, RICO.identifier, Literal(self.entity.record_id))
        yield (self.uri, RICO.hasInstantiation, self.inst_uri)
        yield (self.agent_uri, RICO.isOrWasDescribedBy, self.uri)
        yield (self.uri, RICO.describesOrDescribed, self.agent_uri)
        yield (self.uri, RDF.type, RICO.Record)
        yield (
            self.uri,
            RICO.hasDocumentaryForm,
            RICO_FORM.AuthorityRecord,
        )

        rset = self._cw.execute(
            "Any A, TYPE, START, END, AGENTTYPE, AGENT, DESCR WHERE"
            "A is Activity, A generated X, X is AuthorityRecord, X eid %(eid)s,"
            "A type TYPE, A start START, A end END, A agent_type AGENTTYPE,"
            "A agent AGENT, A description DESCR",
            {"eid": self.entity.eid},
        )
        if rset:
            for act_eid, act_type, start, end, agent_type, agent, description in rset:
                activity_uri = self._cw.entity_from_eid(act_eid).cw_adapt_to("rdf").uri

                yield (self.uri, RICO.isOrWasAffectedBy, activity_uri)
                yield (activity_uri, RDF.type, RICO.Activity)
                yield (
                    activity_uri,
                    RICO.name,
                    Literal(f"{act_type} ({agent}, {agent_type})"),
                )
                if start:
                    yield (activity_uri, RICO.beginningDate, Literal(start))
                if start:
                    yield (activity_uri, RICO.endDate, Literal(end))
                if description:
                    yield (
                        activity_uri,
                        RICO.descriptiveNote,
                        Literal(remove_html_tags(description)),
                    )

        sources = self._cw.execute(
            "Any TITLE, URL WHERE"
            "S is EACSource, S source_agent X, X is AuthorityRecord, X eid %(eid)s,"
            "S title TITLE, S url URL",
            {"eid": self.entity.eid},
        )
        if sources:
            for title, url in sources:
                if url is not None and _is_valid_uri(url):
                    yield (self.uri, RICO.hasSource, URIRef(url))
                elif title:
                    yield (self.uri, RICO.source, Literal(title))

    def triples(self):
        yield from self.record_triples()
        yield from self.agent_triples()
