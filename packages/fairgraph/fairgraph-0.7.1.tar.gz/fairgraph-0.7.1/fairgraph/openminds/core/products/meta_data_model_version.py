"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObject, IRI
from fairgraph.fields import Field




class MetaDataModelVersion(KGObject):
    """

    """
    default_space = "metadatamodel"
    type = ["https://openminds.ebrains.eu/core/MetaDataModelVersion"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("name", str, "vocab:fullName", multiple=False, required=False,
              doc="Whole, non-abbreviated name of the meta data model version."),
        Field("alias", str, "vocab:shortName", multiple=False, required=True,
              doc="Shortened or fully abbreviated name of the meta data model version."),
        Field("accessibility", "openminds.controlledterms.ProductAccessibility", "vocab:accessibility", multiple=False, required=True,
              doc="Level to which something is accessible to the meta data model version."),
        Field("copyright", "openminds.core.Copyright", "vocab:copyright", multiple=False, required=False,
              doc="Exclusive and assignable legal right of an originator to reproduce, publish, sell, or distribute the matter and form of a creative work for a defined time period."),
        Field("custodians", ["openminds.core.Organization", "openminds.core.Person"], "vocab:custodian", multiple=True, required=False,
              doc="The 'custodian' is a legal person who is responsible for the content and quality of the data, metadata, and/or code of a research product."),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the meta data model version."),
        Field("developers", ["openminds.core.Organization", "openminds.core.Person"], "vocab:developer", multiple=True, required=False,
              doc="Legal person that creates or improves products or services (e.g., software, applications, etc.)."),
        Field("digital_identifier", ["openminds.core.DOI", "openminds.core.SWHID"], "vocab:digitalIdentifier", multiple=False, required=False,
              doc="Digital handle to identify objects or legal persons."),
        Field("full_documentation", ["openminds.core.DOI", "openminds.core.File", "openminds.core.URL"], "vocab:fullDocumentation", multiple=False, required=True,
              doc="Non-abridged instructions, comments, and information for using a particular product."),
        Field("funding", "openminds.core.Funding", "vocab:funding", multiple=True, required=False,
              doc="Money provided by a legal person for a particular purpose."),
        Field("homepage", "openminds.core.URL", "vocab:homepage", multiple=False, required=False,
              doc="Main website of the meta data model version."),
        Field("how_to_cite", str, "vocab:howToCite", multiple=False, required=False,
              doc="Preferred format for citing a particular object or legal person."),
        Field("is_alternative_version_of", "openminds.core.MetaDataModelVersion", "vocab:isAlternativeVersionOf", multiple=True, required=False,
              doc="Reference to an original form where the essence was preserved, but presented in an alternative form."),
        Field("is_new_version_of", "openminds.core.MetaDataModelVersion", "vocab:isNewVersionOf", multiple=False, required=False,
              doc="Reference to a previous (potentially outdated) particular form of something."),
        Field("keywords", ["openminds.controlledterms.ActionStatusType", "openminds.controlledterms.AgeCategory", "openminds.controlledterms.AnatomicalAxesOrientation", "openminds.controlledterms.AnatomicalPlane", "openminds.controlledterms.AnnotationType", "openminds.controlledterms.AtlasType", "openminds.controlledterms.BiologicalOrder", "openminds.controlledterms.BiologicalSex", "openminds.controlledterms.BreedingType", "openminds.controlledterms.CellCultureType", "openminds.controlledterms.CellType", "openminds.controlledterms.ContributionType", "openminds.controlledterms.CranialWindowType", "openminds.controlledterms.CriteriaQualityType", "openminds.controlledterms.DataType", "openminds.controlledterms.DeviceType", "openminds.controlledterms.Disease", "openminds.controlledterms.DiseaseModel", "openminds.controlledterms.EthicsAssessment", "openminds.controlledterms.ExperimentalApproach", "openminds.controlledterms.FileBundleGrouping", "openminds.controlledterms.FileRepositoryType", "openminds.controlledterms.FileUsageRole", "openminds.controlledterms.GeneticStrainType", "openminds.controlledterms.Handedness", "openminds.controlledterms.Language", "openminds.controlledterms.Laterality", "openminds.controlledterms.MeasuredQuantity", "openminds.controlledterms.MetaDataModelType", "openminds.controlledterms.ModelAbstractionLevel", "openminds.controlledterms.ModelScope", "openminds.controlledterms.MolecularEntity", "openminds.controlledterms.OperatingDevice", "openminds.controlledterms.OperatingSystem", "openminds.controlledterms.Organ", "openminds.controlledterms.PatchClampVariation", "openminds.controlledterms.PreparationType", "openminds.controlledterms.ProductAccessibility", "openminds.controlledterms.ProgrammingLanguage", "openminds.controlledterms.QualitativeOverlap", "openminds.controlledterms.SemanticDataType", "openminds.controlledterms.Service", "openminds.controlledterms.SoftwareApplicationCategory", "openminds.controlledterms.SoftwareFeature", "openminds.controlledterms.Species", "openminds.controlledterms.StimulationApproach", "openminds.controlledterms.StimulusType", "openminds.controlledterms.SubcellularEntity", "openminds.controlledterms.SubjectAttribute", "openminds.controlledterms.Technique", "openminds.controlledterms.TermSuggestion", "openminds.controlledterms.Terminology", "openminds.controlledterms.TissueSampleAttribute", "openminds.controlledterms.TissueSampleType", "openminds.controlledterms.TypeOfUncertainty", "openminds.controlledterms.UBERONParcellation", "openminds.controlledterms.UnitOfMeasurement", "openminds.publications.LivePaperResourceType", "openminds.publications.LivePaperSectionType"], "vocab:keyword", multiple=True, required=False,
              doc="Significant word or concept that are representative of the meta data model version."),
        Field("license", "openminds.core.License", "vocab:license", multiple=False, required=True,
              doc="Grant by a party to another party as an element of an agreement between those parties that permits to do, use, or own something."),
        Field("other_contributions", "openminds.core.Contribution", "vocab:otherContribution", multiple=True, required=False,
              doc="Giving or supplying of something (such as money or time) as a part or share other than what is covered elsewhere."),
        Field("related_publications", ["openminds.core.DOI", "openminds.core.HANDLE", "openminds.core.ISBN"], "vocab:relatedPublication", multiple=True, required=False,
              doc="Reference to something that was made available for the general public to see or buy."),
        Field("release_date", date, "vocab:releaseDate", multiple=False, required=True,
              doc="Fixed date on which a product is due to become or was made available for the general public to see or buy"),
        Field("repository", "openminds.core.FileRepository", "vocab:repository", multiple=False, required=False,
              doc="Place, room, or container where something is deposited or stored."),
        Field("serialization_formats", "openminds.core.ContentType", "vocab:serializationFormat", multiple=True, required=False,
              doc="Form in which a particular data structure or object state is translated to for storage."),
        Field("specification_formats", "openminds.core.ContentType", "vocab:specificationFormat", multiple=True, required=False,
              doc="Form in which a particular data structure or object state is specified in."),
        Field("support_channels", str, "vocab:supportChannel", multiple=True, required=False,
              doc="Way of communication used to interact with users or customers."),
        Field("type", "openminds.controlledterms.MetaDataModelType", "vocab:type", multiple=False, required=True,
              doc="Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to."),
        Field("version_identifier", str, "vocab:versionIdentifier", multiple=False, required=True,
              doc="Term or code used to identify the version of something."),
        Field("version_innovation", str, "vocab:versionInnovation", multiple=False, required=True,
              doc="Documentation on what changed in comparison to a previously published form of something."),

    ]
    existence_query_fields = ('alias', 'version_identifier')
