
EXTRA_DIST =  

# Warning: This is an automatically generated file, do not edit!

if ENABLE_DEBUG
ASSEMBLY_COMPILER_COMMAND = dmcs
ASSEMBLY_COMPILER_FLAGS =  -noconfig -codepage:utf8 -warn:4 -optimize- -debug "-define:DEBUG"
ASSEMBLY = bin/Debug/ChatterBotAPITest.exe
ASSEMBLY_MDB = $(ASSEMBLY).mdb
COMPILE_TARGET = exe
PROJECT_REFERENCES =  \
	../ChatterBotAPI/bin/Debug/ChatterBotAPI.dll
BUILD_DIR = bin/Debug

CHATTERBOTAPITEST_EXE_MDB_SOURCE=bin/Debug/ChatterBotAPITest.exe.mdb
CHATTERBOTAPITEST_EXE_MDB=$(BUILD_DIR)/ChatterBotAPITest.exe.mdb
CHATTERBOTAPI_DLL_SOURCE=../ChatterBotAPI/bin/Debug/ChatterBotAPI.dll
CHATTERBOTAPI_DLL_MDB_SOURCE=../ChatterBotAPI/bin/Debug/ChatterBotAPI.dll.mdb
CHATTERBOTAPI_DLL_MDB=$(BUILD_DIR)/ChatterBotAPI.dll.mdb

endif

if ENABLE_RELEASE
ASSEMBLY_COMPILER_COMMAND = dmcs
ASSEMBLY_COMPILER_FLAGS =  -noconfig -codepage:utf8 -warn:4 -optimize-
ASSEMBLY = bin/Release/ChatterBotAPITest.exe
ASSEMBLY_MDB = 
COMPILE_TARGET = exe
PROJECT_REFERENCES =  \
	../ChatterBotAPI/bin/Release/ChatterBotAPI.dll
BUILD_DIR = bin/Release

CHATTERBOTAPITEST_EXE_MDB=
CHATTERBOTAPI_DLL_SOURCE=../ChatterBotAPI/bin/Release/ChatterBotAPI.dll
CHATTERBOTAPI_DLL_MDB=

endif

AL=al
SATELLITE_ASSEMBLY_NAME=$(notdir $(basename $(ASSEMBLY))).resources.dll

PROGRAMFILES = \
	$(CHATTERBOTAPITEST_EXE_MDB) \
	$(CHATTERBOTAPI_DLL) \
	$(CHATTERBOTAPI_DLL_MDB)  

BINARIES = \
	$(CHATTERBOTAPITEST)  


RESGEN=resgen2
	
all: $(ASSEMBLY) $(PROGRAMFILES) $(BINARIES) 

FILES = \
	Main.cs \
	Properties/AssemblyInfo.cs 

DATA_FILES = 

RESOURCES = 

EXTRAS = \
	Properties \
	chatterbotapitest.in 

REFERENCES =  \
	System

DLL_REFERENCES = 

CLEANFILES = $(PROGRAMFILES) $(BINARIES) 

include $(top_srcdir)/Makefile.include

CHATTERBOTAPI_DLL = $(BUILD_DIR)/ChatterBotAPI.dll
CHATTERBOTAPITEST = $(BUILD_DIR)/chatterbotapitest

$(eval $(call emit-deploy-target,CHATTERBOTAPI_DLL))
$(eval $(call emit-deploy-target,CHATTERBOTAPI_DLL_MDB))
$(eval $(call emit-deploy-wrapper,CHATTERBOTAPITEST,chatterbotapitest,x))


$(eval $(call emit_resgen_targets))
$(build_xamlg_list): %.xaml.g.cs: %.xaml
	xamlg '$<'

$(ASSEMBLY_MDB): $(ASSEMBLY)

$(ASSEMBLY): $(build_sources) $(build_resources) $(build_datafiles) $(DLL_REFERENCES) $(PROJECT_REFERENCES) $(build_xamlg_list) $(build_satellite_assembly_list)
	mkdir -p $(shell dirname $(ASSEMBLY))
	$(ASSEMBLY_COMPILER_COMMAND) $(ASSEMBLY_COMPILER_FLAGS) -out:$(ASSEMBLY) -target:$(COMPILE_TARGET) $(build_sources_embed) $(build_resources_embed) $(build_references_ref)
