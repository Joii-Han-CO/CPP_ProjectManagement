// define some type
#pragma once

// interface args type
#define IN
#define OUT
#define IN_OUT

#define INLINE inline

// Windows
#ifdef WIN32
  #ifdef $(--NAMESPACE--)_STATIC
    // static
    #define $(--NAMESPACE--)_LIB_EXP extern
  #else
    // dynamic
    #ifdef $(--NAMESPACE--)_LIB  // input
      #define $(--NAMESPACE--)_LIB_EXP __declspec(dllexport)
    #else  // output
      #define $(--NAMESPACE--)_LIB_EXP __declspec(dllimport)
    #endif
  #endif
#else
  #define $(--NAMESPACE--)_LIB_EXP
#endif
