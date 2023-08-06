#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "HELICS::helicsSharedLib" for configuration "Release"
set_property(TARGET HELICS::helicsSharedLib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(HELICS::helicsSharedLib PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libhelicsSharedLib.so.2.8.1"
  IMPORTED_SONAME_RELEASE "libhelicsSharedLib.so.2"
  )

list(APPEND _IMPORT_CHECK_TARGETS HELICS::helicsSharedLib )
list(APPEND _IMPORT_CHECK_FILES_FOR_HELICS::helicsSharedLib "${_IMPORT_PREFIX}/lib64/libhelicsSharedLib.so.2.8.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
