"""cubicweb-eac application package

Implementation of Encoded Archival Context for CubicWeb
"""

from functools import partial
from cubicweb_compound import CompositeGraph


# EAC mappings

TYPE_MAPPING = {
    "corporateBody": "authority",
    "person": "person",
    "family": "family",
}

MAINTENANCETYPE_MAPPING = {
    "created": "create",
    "revised": "modify",
}

# Order matters for this one in order to export correctly
ADDRESS_MAPPING = [
    ("voie", "street"),
    ("postalcode", "postalcode"),
    ("city", "city"),
]


AuthorityRecordGraph = partial(CompositeGraph, skiprtypes=("generated", "used"))
