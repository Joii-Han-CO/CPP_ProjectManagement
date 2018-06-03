include(CMakeParseArguments)

################################################################
# 创建项目
function(CreateLibProject)

################################################################
# 解析参数
  set(options OPTIONAL FAST)
  set(oneValueArgs name namespace folder lib_type)
  set(multiValueArgs include_dirs include_files include_cpps)
  
  CMAKE_PARSE_ARGUMENTS(
    ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN}
  )
  Add_Definitions(-DUNICODE -D_UNICODE)

################################################################


################################################################
# 创建工程
  # create project
  project(${ARG_name})
  
  # output
  message(Project Name: ${ARG_name})
  message(Project Namespace ${ARG_namespace})
  message(Project Folder: ${ARG_folder})
  message(Project Dir: ${PROJECT_SOURCE_DIR})

################################################################


################################################################
# 设置各个变量
  # project path
  set(__cpp_dir ${PROJECT_SOURCE_DIR}/../../../src/${ARG_folder}/${ARG_name}/)
  set(__incldue ${PROJECT_SOURCE_DIR}/../../../src/include/)
  
  # include dirs
  set(__include_dirs_buf
    ${ARG_include_dirs}
    ${__cpp_dir}
    ${__incldue})
  
  # header file list
  set(__def_includefiles
    ${__cpp_dir}stdafx.h
    ${__incldue}/${ARG_namespace}_${ARG_name}.h
    ${__incldue}/${ARG_namespace}_${ARG_name}.hpp)
  source_group("include" FILES ${__def_includefiles})
  
  # cpp file list
  set(__def_cppfiles
    ${__cpp_dir}/stdafx.cpp
    ${__cpp_dir}/${ARG_namespace}_${ARG_name}.cpp)
  source_group("source" FILES ${__def_cppfiles})
  
################################################################


################################################################
# 添加文件
    
  # include dirs
  include_directories(${ARG_name} ${__include_dirs_buf})
  
  # add src files
  add_library(${ARG_name} ${ARG_lib_type}
              ${__def_includefiles}
              ${ARG_include_files}
              ${__def_cppfiles}
              ${ARG_include_cpps}
  )
  
  set(__compile_def $(--NAMESPACE--)_LIB)
  if (${__prj_lib_type} STREQUAL "STATIC")
    set(__compile_def ${__compile_def} $(--NAMESPACE--)_STATIC)
  endif()
  target_compile_definitions(
            ${ARG_name}
            PRIVATE
            ${__compile_def})

################################################################


################################################################
# 设置工程目录
  set(prj_path ${ARG_folder}/${ARG_name})
  set_target_properties(${ARG_name} PROPERTIES FOLDER ${prj_path})
################################################################

endfunction(CreateLibProject)
################################################################


################################################################
# 创建测试项目
function(CreateTestProject)

################################################################
# 解析参数
  set(options OPTIONAL FAST)
  set(oneValueArgs name namespace folder)
  set(multiValueArgs include_dirs include_files include_cpps)
  
  CMAKE_PARSE_ARGUMENTS(
    ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN}
  )
  Add_Definitions(-DUNICODE -D_UNICODE)
  
################################################################


################################################################
# 创建工程
  # create project
  set(ARG_name_test ${ARG_name}_test)
  project(${ARG_name_test})
  
  # output
  message(Project Name: ${ARG_name_test})
  message(Project Namespace ${ARG_namespace})
  message(Project Folder: ${ARG_folder})
  message(Project Dir: ${PROJECT_SOURCE_DIR})

################################################################


################################################################
# 设置各个变量
  # project path
  set(__cpp_dir ${PROJECT_SOURCE_DIR}/../../../src/${ARG_folder}/${ARG_name}/test/)
  set(__incldue ${PROJECT_SOURCE_DIR}/../../../src/include/)
  
  # include dirs
  set(__include_dirs_buf
    ${ARG_include_dirs}
    ${__cpp_dir}
    ${__incldue})
  
  # header file list
  set(__def_includefiles
    ${__cpp_dir}stdafx.h
    ${__cpp_dir}/test_${ARG_name}.h)
  source_group("include" FILES ${__def_includefiles})
  
  # cpp file list
  set(__def_cppfiles
    ${__cpp_dir}/stdafx.cpp
    ${__cpp_dir}/test_${ARG_name}.cpp)
  source_group("source" FILES ${__def_cppfiles})
  
################################################################


################################################################
# 添加文件
  # include dirs
  include_directories(${ARG_name_test} ${__include_dirs_buf})
  
  # add src files
  add_executable(${ARG_name_test}
                ${__def_includefiles}
                ${ARG_include_files}
                ${__def_cppfiles}
                ${ARG_include_cpps}
  )
  
  target_compile_definitions(
            ${ARG_name_test}
            PRIVATE
            $(--NAMESPACE--)_LIB)

################################################################


################################################################
# 设置工程目录
  set(prj_path ${ARG_folder}/${ARG_name})
  set_target_properties(${ARG_name_test} PROPERTIES FOLDER ${prj_path})
################################################################
  
endfunction(CreateTestProject)
################################################################

