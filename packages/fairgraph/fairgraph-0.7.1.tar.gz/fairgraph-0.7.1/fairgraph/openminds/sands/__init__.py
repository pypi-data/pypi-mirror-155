import sys
import inspect
from ...base_v3 import KGObject

from .non_atlas.custom_coordinate_space import CustomCoordinateSpace
from .non_atlas.custom_annotation import CustomAnnotation
from .non_atlas.custom_anatomical_entity import CustomAnatomicalEntity
from .miscellaneous.qualitative_relation_assessment import QualitativeRelationAssessment
from .miscellaneous.quantitative_relation_assessment import QuantitativeRelationAssessment
from .miscellaneous.coordinate_point import CoordinatePoint
from .atlas.parcellation_entity import ParcellationEntity
from .atlas.common_coordinate_space import CommonCoordinateSpace
from .atlas.parcellation_terminology import ParcellationTerminology
from .atlas.parcellation_terminology_version import ParcellationTerminologyVersion
from .atlas.brain_atlas import BrainAtlas
from .atlas.atlas_annotation import AtlasAnnotation
from .atlas.brain_atlas_version import BrainAtlasVersion
from .atlas.parcellation_entity_version import ParcellationEntityVersion


def list_kg_classes():
    """List all KG classes defined in this module"""
    return [obj for name, obj in inspect.getmembers(sys.modules[__name__])
           if inspect.isclass(obj) and issubclass(obj, KGObject) and obj.__module__.startswith(__name__)]
