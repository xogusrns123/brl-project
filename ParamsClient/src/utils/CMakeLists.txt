add_library(memory_utils STATIC memory_utils.cu)
set_property(TARGET memory_utils PROPERTY POSITION_INDEPENDENT_CODE  ON)
set_property(TARGET memory_utils PROPERTY CUDA_RESOLVE_DEVICE_SYMBOLS  ON)
if (AWS_SDK_PATH)
    target_link_libraries(memory_utils PUBLIC -lnvToolsExt aws-cpp-sdk-core aws-cpp-sdk-s3)
else()
    target_link_libraries(memory_utils PUBLIC -lnvToolsExt)
endif()

add_library(mpi_utils STATIC mpi_utils.cc)
set_property(TARGET mpi_utils PROPERTY POSITION_INDEPENDENT_CODE  ON)
set_property(TARGET mpi_utils PROPERTY CUDA_RESOLVE_DEVICE_SYMBOLS  ON)
# if (BUILD_MULTI_GPU)
    target_link_libraries(mpi_utils PUBLIC -lmpi)
# endif()

add_library(nccl_utils STATIC nccl_utils.cc)
set_property(TARGET nccl_utils PROPERTY POSITION_INDEPENDENT_CODE  ON)
set_property(TARGET nccl_utils PROPERTY CUDA_RESOLVE_DEVICE_SYMBOLS  ON)
# if (BUILD_MULTI_GPU)
    target_link_libraries(nccl_utils PUBLIC -lnccl mpi_utils)
# endif()

add_library(tcp_utils STATIC tcp_utils.cc)
set_property(TARGET tcp_utils PROPERTY POSITION_INDEPENDENT_CODE ON)
