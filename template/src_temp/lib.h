#pragma once
#include "$(--namespace--)_type_def.h"


#ifdef __cplusplus
extern "C" {
  namespace $(--namespace--) {
  namespace $(--prj_name--) {
#endif

  // 测试接口
  $(--NAMESPACE--)_LIB_EXP bool Test_$(--prj_name--)_C(IN int test_args);

#ifdef __cplusplus
  }
  }
}
#endif
