#include "stdafx.h"
#include "test_$(--prj_name--).h"
#include "$(--namespace--)_$(--prj_name--).h"
#include "$(--namespace--)_$(--prj_name--).hpp"

#pragma region namespace
namespace test {
#pragma endregion

  void test_C(){
    std::cout << "test_$(--prj_name--)_C Begin:" << std::endl;
    $(--namespace--)::$(--prj_name--)::Test_$(--prj_name--)_C(8);
    std::cout << "test_$(--prj_name--)_C Begin:" << std::endl;
  }

  void test_CPP(){
    std::cout << "test_$(--prj_name--)_CPP Begin:" << std::endl;
    $(--namespace--)::$(--prj_name--)::Test_$(--prj_name--)_CPP(8);
    std::cout << "test_$(--prj_name--)_CPP Begin:" << std::endl;
  }

#pragma region namespace
}
#pragma endregion

int main() {
  
  test::test_C();
  test::test_CPP();

  return 0;
}
