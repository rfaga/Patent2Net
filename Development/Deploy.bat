﻿REM This script is use to deploy from my own directory to git-hub connected one
REM this is also a comment of different programs :-)
REM useful things
copy /y requete.cql ..\Patent2Net\Patent2Net\Development
copy /y cacert.pem ..\Patent2Net\Patent2Net\Development
copy /y CollecteEtTRaite.bat ..\Patent2Net\Patent2Net\Development
copy /y Compile.bat ..\Patent2Net\Patent2Net\Development
copy /y Deploy.bat ..\Patent2Net\Patent2Net\Development
REM HTML Formating : Datatable
copy /y ScriptSearch.js ..\Patent2Net\Patent2Net\Development
copy /y ModeleDist.html ..\Patent2Net\Patent2Net\Development\Modele.html
copy /y ModeleFamilleDist.html ..\Patent2Net\Patent2Net\Development\ModeleFamille.html
copy /y ScriptSearch.js ..\Patent2Net\Patent2Net\Development\
REM HTML Formating : ¨Pivotable
copy /y PivotDist.html ..\Patent2Net\Patent2Net\Development\Pivot.html
copy /y ModeleFamillePivot.html ..\Patent2Net\Patent2Net\Development\ModeleFamillePivot.html
REM HTML Formating : Cartography
copy /y countries.json ..\Patent2Net\Patent2Net\Development
copy /y ModeleCarto.html ..\Patent2Net\Patent2Net\Development
copy /y NameCountryMap.csv ..\Patent2Net\Patent2Net\Development
REM HTML Formating : NetWorks
copy /y Graphe.html ..\Patent2Net\Patent2Net\Development
copy /y config.js ..\Patent2Net\Patent2Net\Development
copy /y NameCountryMap.csv ..\Patent2Net\Patent2Net\Development
REM HTML Formating : Launching firefox
copy /y OpenNav.bat ..\Patent2Net\Patent2Net\Development
REM HTML Formating : General index
REM THE MENU in root
copy /y ..\index.html dist
REM content of analyses
copy /y index.js dist\Patent2Net\ 
REM Menus for each analyse
copy /y ModeleIndex.html ..\Patent2Net\Patent2Net\Development\ModeleIndex.html
copy /y ModeleContenuIndex.html ..\Patent2Net\Patent2Net\Development\ModeleContenuIndex.html
REM HTML Formating : External libraries
mkdir ..\Patent2Net\Patent2Net\Development\extensions
mkdir ..\Patent2Net\Patent2Net\Development\media
echo off
xcopy /y /s media ..\Patent2Net\Patent2Net\Development\media\
xcopy /y /s extensions ..\Patent2Net\Patent2Net\Development\extensions\
echo on
REM Main programs
REM Main programs:Collectors
copy OPSGatherPatentsV2.py ..\Patent2Net\Patent2Net\Development
copy OPSGatherAugment-Families.py ..\Patent2Net\Patent2Net\Development
copy OPSGatherContentsv1-Iramuteq.py ..\Patent2Net\Patent2Net\Development

REM Main programs:Networks productions
copy P2N-Authors.py ..\Patent2Net\Patent2Net\Development
copy P2N-AuthorsApplicants.py ..\Patent2Net\Patent2Net\Development
copy P2N-Applicants.py ..\Patent2Net\Patent2Net\Development
copy P2N-ApplicantsCrossTech.py ..\Patent2Net\Patent2Net\Development
copy P2N-CountryCrossTech.py ..\Patent2Net\Patent2Net\Development
copy P2N-InventorCrossTech.py ..\Patent2Net\Patent2Net\Development
copy P2N-CrossTech.py ..\Patent2Net\Patent2Net\Development
copy P2N-Families.py ..\Patent2Net\Patent2Net\Development
copy P2N-FamiliesHierarc.py ..\Patent2Net\Patent2Net\Development
copy P2N-V5.py ..\Patent2Net\Patent2Net\Development
REM Main programs:Formating exports
copy FusionIramuteq.py ..\Patent2Net\Patent2Net\Development
copy FormateExport.py ..\Patent2Net\Patent2Net\Development
copy FormateExportFamilies.py ..\Patent2Net\Patent2Net\Development
copy CartographyCountry.py ..\Patent2Net\Patent2Net\Development

REM Tools (fusion two collect)
copy Fusion.py ..\Patent2Net\Patent2Net\Development
copy Interface.py ..\Patent2Net\Patent2Net\Development
copy Interface2.py ..\Patent2Net\Patent2Net\Development
REM Libraries
copy /y Ops2.py ..\Patent2Net\Patent2Net\Development\
copy /y Ops3.py ..\Patent2Net\Patent2Net\Development\
copy /y Ops2NetUtils.py ..\Patent2Net\Patent2Net\Development
copy /y Ops2NetUtils2.py ..\Patent2Net\Patent2Net\Development

REM Externals Libraries
copy Diverging_Map.py ..\Patent2Net\Patent2Net\Development
copy /y Networkx_functs.py ..\Patent2Net\Patent2Net\Development
REM next one is unused and buggy... sometime I'll try to implement nooverlap and a good force atlas algorithm
REM copy /y forceatlas.py ..\Patent2Net\Patent2Net\Development
