### Context
* Created: November 2021
* Author: Renier Kramer, renier.kramer@hdsr.nl
* Python version: 3.7

### Description
A python project that you can use to read the HDSR FEWS-WIS configuration. 
It serves an interface (python objects) for configuration files (.xmls and .csv).

### Usage (10 examples)
```
--------------------------------------------------------------------------------
# install dependencies (with pip or conda)
pip install hdsr-wis-config-reader
conda install hdsr-wis-config-reader --channel hdsr-mid

# prepare the examples
>>> from hdsr_wis_config_reader import XmlReader, FewsConfigReader, LocationSetCollection, IdMappingCollection, \
    merge_startenddate_github_with_idmap
>>> from hdsr_wis_config_reader.idmappings.columns import IdMapCols
>>> import pathlib  # dependency of hdsr-wis-config-reader
>>> config_dir = pathlib.Path(<path_to_fews_config_dir>)  # this points to the FEWS <region_home>/config dir
>>> fews_config = FewsConfigReader(path=config_dir)
>>> location_sets = LocationSetCollection(fews_config=fews_config)
>>> id_mappings = IdMappingCollection(fews_config=fews_config)
--------------------------------------------------------------------------------
# 1. Get the absoluate path to a config file
>>> fews_config.RegionConfigFiles["Filters"]
# ../<path_to_fews_config_dir>/RegionConfigFiles/Filters.xml'
--------------------------------------------------------------------------------
# 2. Get hoofdlocationset names
>>> location_sets.hoofd_loc.name
# 'hoofdlocaties'
>>> location_sets.hoofd_loc.csv_filename
'oppvlwater_hoofdloc'
>>> location_sets.hoofd_loc.fews_name
'OPVLWATER_HOOFDLOC'
--------------------------------------------------------------------------------
# 3. Get a dataframe of parameters
>>> fews_config.get_parameters()
# GROUP     DESCRIPTION PARAMETERTYPE   UNIT    VALUERESOLUTION USESDATUM   ID  NAME                                SHORTNAME
# Biomassa              instantaneous   kg/ha   0.1                         B.d Biomassa productie [kg/ha] - dag    Biomassa productie [kg/ha] - dag
# Biomassa              instantaneous   kg/ha   0.1                         B.m Biomassa productie [kg/ha] - maand  Biomassa productie [kg/ha] - maand
# etc...
--------------------------------------------------------------------------------       
# 4. Get a geodataframe with hoofd locations (note that geomeometry height (z) gets -9999 when if Z is nan)
>>> location_sets.hoofd_loc.geo_df
# LOC_ID      LOC_NAME                            X       Y       Z       ALLE_TYPES          START       ...     geometry
# KW100110    WIJKERSLOOT_1001-K_WIJKERSLOOT      150501  442988  2.87    krooshek/pompvijzel 19970101    ...     POINT Z (150501 442988 2.87)
# KW100120    WIJKERSLOOT_1001-K_WIJKERSLOOT STUW 150439  442885  nan     stuw                20120321    ...     POINT Z (150439 442885 -9999)
# etc...
--------------------------------------------------------------------------------
# 5. Get the validation rules for sublocations
>>> location_sets.sub_loc.validation_rules
# [
#   {'parameter': 'H.R.', 'extreme_values': {'hmax': 'HR1_HMAX', 'hmin': 'HR1_HMIN'}}, 
#   {'parameter': 'H2.R.', 'extreme_values': {'hmax': 'HR2_HMAX', 'hmin': 'HR2_HMIN'}},
#   etc..
# ]
--------------------------------------------------------------------------------
# 6. Get the attribute files for waterstand locations 
>>> location_sets.waterstandloc.attrib_files
# [
#   {   'csvFile': 'oppvlwater_langsprofielen', 
#       'id': '%LOC_ID%', 
#       'attribute': [
#           {'number': '%Langsprofiel_Kromme_Rijn%', 'id': 'Langsprofiel_Kromme_Rijn'}, 
#           {'number': '%Langsprofiel_Caspargouwse_Wetering%', 'id': 'Langsprofiel_Caspargouwse_Wetering'},
#   etc...
--------------------------------------------------------------------------------
# 7. Get filtered idmapping (you can filter on one or more args: {ex_loc, ex_par, int_loc, int_par}): 
>>> df_idmap = id_mappings.idmap_all.get_filtered_df(int_loc="KW761001")
# externalLocation  externalParameter   internalLocation    internalParameter   source              histtag
# 610               Q1                  KW761001            Q.G.0               IdOPVLWATER         610_Q1
# 7610              Q1                  KW761001            Q.G.0               IdOPVLWATER         7610_Q1
# 610               Q1                  KW761001            Q.G.0               IdOPVLWATER_HYMOS   610_Q1
# To filter only op idmappping opperlvakte water
>>> df_idmap = id_mappings.idmap_opvl_water.get_filtered_df(ex_loc='001')
--------------------------------------------------------------------------------
# 8. Get all external parameters in the groundwater idmapping
>>> id_mappings.idmap_grondwater_caw.get_filtered_column_values(
        make_result_unique=True,
        target_column=IdMapCols.ex_par,
    )  
# ['1GW', 'GW1', 'GW2', 'GW3', 'HB1', 'HB2', 'HB3', 'HB4', 'HB5', 'HB6', 'HB7', 'HB8']
--------------------------------------------------------------------------------
# 9. Read an id_mapping xml file into dataframe without a FEWS configuration (filtering also possible)
>>> idmap_file_path = Path(<path_to_fews_config_dir>) / "IdMapFiles" / "IdOPVLWATER.xml"
>>> df_idmap_oppvl = IdMappingCollection.get_idmap_df_via_path(file_path=idmap_file_path)
>>> df_filtered = df_idmap_oppvl.get_filtered_df(int_par="H.G.0")
--------------------------------------------------------------------------------
# 10. Read and merge id_mapping + startendate files (or choose your own startendate file with merge_startenddate_idmap())
>>> df = merge_startenddate_github_with_idmap(df_idmap=id_mappings.idmap_all)
#  series               start                 end         filename_start           filename_end externalLocation externalParameter internalLocation  internalParameter       idmap_source
# 001_ES1 2012-03-21 15:00:00 2012-06-04 16:10:32  HDSR_CAW_201205091959  HDSR_CAW_201206042000              001               ES1              NaN                NaN                NaN   
# 001_ES2 2012-03-21 15:00:00 2012-05-26 13:29:40  HDSR_CAW_201204262000  HDSR_CAW_201205262000              001               ES2              NaN                NaN                NaN    
# 001_FQ1 2010-04-27 23:59:59 2018-03-27 13:15:00  HDSR_CAW_201204262000  HDSR_CAW_201803271320              001               FQ1         KW100111                F.0        IdOPVLWATER    
# 001_FQ1 2010-04-27 23:59:59 2018-03-27 13:15:00  HDSR_CAW_201204262000  HDSR_CAW_201803271320              001               FQ1         KW100111               F.15  IdOPVLWATER_HYMOS    
# 001_HB1 2010-04-27 23:59:59 2018-03-27 13:15:00  HDSR_CAW_201204262000  HDSR_CAW_201803271320              001               HB1         OW100102              H.G.0        IdOPVLWATER 
```

### License 
[MIT][mit]

[mit]: https://github.com/hdsr-mid/hdsr_wis_config_reader/blob/main/LICENSE.txt

### Contributions
All contributions, bug reports, bug fixes, documentation improvements, enhancements 
and ideas are welcome on https://github.com/hdsr-mid/hdsr_wis_config_reader/issues

### Test Coverage
```
---------- coverage: platform win32, python 3.7.11-final-0 -----------
Name                                                    Stmts   Miss  Cover
---------------------------------------------------------------------------
hdsr_wis_config_reader\__init__.py                         14      0   100%
hdsr_wis_config_reader\constants.py                        17      1    94%
hdsr_wis_config_reader\idmappings\collection.py            79      4    95%
hdsr_wis_config_reader\idmappings\columns.py               87     13    85%
hdsr_wis_config_reader\idmappings\custom_dataframe.py      28      1    96%
hdsr_wis_config_reader\idmappings\files.py                  9      1    89%
hdsr_wis_config_reader\idmappings\sections.py              10      1    90%
hdsr_wis_config_reader\idmappings\utils.py                 11      0   100%
hdsr_wis_config_reader\location_sets\base.py               90      9    90%
hdsr_wis_config_reader\location_sets\collection.py         54      3    94%
hdsr_wis_config_reader\location_sets\columns.py            19      0   100%
hdsr_wis_config_reader\location_sets\hoofd.py              20      2    90%
hdsr_wis_config_reader\location_sets\msw.py                12      1    92%
hdsr_wis_config_reader\location_sets\ow.py                 13      1    92%
hdsr_wis_config_reader\location_sets\ps.py                 12      1    92%
hdsr_wis_config_reader\location_sets\sub.py                27      2    93%
hdsr_wis_config_reader\readers\config_reader.py           154     11    93%
hdsr_wis_config_reader\readers\xml_reader.py               48     10    79%
hdsr_wis_config_reader\startenddate.py                    115     12    90%
hdsr_wis_config_reader\utils.py                            52     10    81%
hdsr_wis_config_reader\validation_rules\__init__.py         4      0   100%
hdsr_wis_config_reader\validation_rules\files.py           35     10    71%
hdsr_wis_config_reader\validation_rules\logic.py           28      0   100%
---------------------------------------------------------------------------
TOTAL                                                     938     93    90%
```

### Conda general tips
#### Build conda environment (on Windows) from any directory using environment.yml:
```
> conda env create --name <conda_env_name> --file <path_to_project>/environment.yml python=<python_version>
> conda info --envs  # verify that <conda_env_name> is in this list 
```
#### Start the application from any directory:
```
> conda activate <conda_env_name>
At any location:
> (<conda_env_name>) python <path_to_project>/main.py
```
#### Test the application:
```
> conda activate <conda_env_name>
> cd <path_to_project>
> pytest  # make sure pytest is installed (conda install pytest)
```
#### List all conda environments on your machine:
```
At any location:
> conda info --envs
```
#### Delete a conda environment:
```
Get directory where environment is located 
> conda info --envs
Remove the enviroment
> conda env remove --name <conda_env_name>
Finally, remove the left-over directory by hand
```
#### Write dependencies to environment.yml:
The goal is to keep the .yml as short as possible (not include sub-dependencies), yet make the environment 
reproducible. Why? If you do 'conda install matplotlib' you also install sub-dependencies like pyqt, qt 
icu, and sip. You should not include these sub-dependencies in your .yml as:
- including sub-dependencies result in an unnecessary strict environment (difficult to solve when conflicting)
- sub-dependencies will be installed when dependencies are being installed
```
> conda activate <conda_env_name>

Recommended:
> conda env export --from-history --no-builds | findstr -v "prefix" > --file <path_to_project>/environment_new.yml   

Alternative:
> conda env export --no-builds | findstr -v "prefix" > --file <path_to_project>/environment_new.yml 

--from-history: 
    Only include packages that you have explicitly asked for, as opposed to including every package in the 
    environment. This flag works regardless how you created the environment (through CMD or Anaconda Navigator).
--no-builds:
    By default, the YAML includes platform-specific build constraints. If you transfer across platforms (e.g. 
    win32 to 64) omit the build info with '--no-builds'.
```
#### Pip and Conda:
If a package is not available on all conda channels, but available as pip package, one can install pip as a dependency.
Note that mixing packages from conda and pip is always a potential problem: conda calls pip, but pip does not know 
how to satisfy missing dependencies with packages from Anaconda repositories. 
```
> conda activate <conda_env_name>
> conda install pip
> pip install <pip_package>
```
The environment.yml might look like:
```
channels:
  - defaults
dependencies:
  - <a conda package>=<version>
  - pip
  - pip:
    - <a pip package>==<version>
```
You can also write a requirements.txt file:
```
> pip list --format=freeze > <path_to_project>/requirements.txt
```
