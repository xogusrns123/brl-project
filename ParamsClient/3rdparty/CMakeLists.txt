add_library(cJSON STATIC cJSON.h cJSON.c)
set_property(TARGET cJSON PROPERTY POSITION_INDEPENDENT_CODE ON)