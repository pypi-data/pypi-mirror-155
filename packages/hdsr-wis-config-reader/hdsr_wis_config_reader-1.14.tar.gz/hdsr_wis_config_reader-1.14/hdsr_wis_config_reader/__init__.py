from hdsr_wis_config_reader import validation_rules
from hdsr_wis_config_reader.idmappings.collection import IdMappingCollection
from hdsr_wis_config_reader.location_sets.collection import LocationSetCollection
from hdsr_wis_config_reader.readers.config_reader import FewsConfigReader
from hdsr_wis_config_reader.readers.xml_reader import XmlReader
from hdsr_wis_config_reader.startenddate import merge_startenddate_github_with_idmap
from hdsr_wis_config_reader.startenddate import merge_startenddate_idmap


# silence flake8 errors
validation_rules = validation_rules
IdMappingCollection = IdMappingCollection
LocationSetCollection = LocationSetCollection
FewsConfigReader = FewsConfigReader
XmlReader = XmlReader
merge_startenddate_idmap = merge_startenddate_idmap
merge_startenddate_github_with_idmap = merge_startenddate_github_with_idmap
