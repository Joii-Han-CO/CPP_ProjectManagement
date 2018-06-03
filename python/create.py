'''
  管理C++工程的工具集
'''

import os
import sys
import shutil
import utility
import git
import argparse


class CreateSln:
  def __init__(self, args):
    self.__last_error = ''
    self.__sln_path = os.path.abspath(args.path + '\\' + args.name)
    self.__sln_name = args.name
    self.__sln_namespace = args.namespace

    self.__temp_path = ''   # 模板路径
    self.__temp_dirs = []   # 需要创建的目录
    self.__temp_files = []  # 模板列表 模板文件路径(相对):输出的路径(绝对)
    self.__temp_macro = []  # 模板中需要替换的宏列表
    self.__temp_info_name = 'temp_info.txt'   # 模板信息列表

    self.__temp_macro.append(['namespace', args.namespace])
    self.__temp_macro.append(['sln_name', args.name])
    self.__temp_macro.append(['NAMESPACE', args.namespace.upper()])
    self.__temp_macro.append(['SLN_NAME', args.name.upper()])

  ##################################################
  # 自检部分

  # 检测各个路径是不是有效
  def __CheckAllPath(self):
    if utility.CheckPath(self.__sln_path) == False:
      self.__last_error = '自检--1路径非法，error:' + utility.GetLastError()
    if utility.CheckPath(self.__sln_path + '\\tools\\python\\') == False:
      self.__last_error = '自检--2路径非法，error:' + utility.GetLastError()

    return True

  # 自检
  def __SelfTest(self):
    print('开始自检')
    if len(self.__sln_path) == 0:
      self.__last_error = '自检--路径不能为空。'
      return False
    if len(self.__sln_name) == 0:
      self.__last_error = '自检--工程名不能为空。'
      return False
    if len(self.__sln_namespace) == 0:
      self.__last_error = '自检--工程命名空间不能为空。'
      return False
    
    self.__temp_path = os.path.dirname(__file__) + '\\..\\template\\'
    self.__temp_path = os.path.abspath(self.__temp_path)
    if os.path.isdir(self.__temp_path) == False:
      self.__last_error = '自检--模板目录不存在'
      return False
    self.__temp_info_name = self.__temp_path + '\\' + self.__temp_info_name
    if os.path.isfile(self.__temp_info_name) == False:
      self.__last_error = '自检--模板对应列表为空'
      return False
    
    if self.__CheckAllPath() == False:
      return False

    return True
  
  # end
  ##################################################

  ##################################################
  # 复制模板

  # 从 temp_info.txt 中解析模板的值 
  def __ParseTempKeyVal(line):
    f_str = '-->'
    i = line.find(f_str)
    if i == -1:
      return None, None
    key = line[: i]
    val = line[ i + len(f_str) :]
    return key, val

  # 获取模板的信息
  def __GetTempInfo(self):
    lines = utility.ReadFileToLines(self.__temp_info_name)
    if lines == None:
      __last_error = '复制模板--读取模板信息错误,Error:' + utility.GetLastError()
      return False
    
    files_list = []
    macro_list = []
    
    temp_type = 0

    # 获取模板信息
    for line in lines:
      line = utility.DelBeginChar(line)
      line = utility.DelEndChar(line)

      if len(line) == 0 or utility.IsComments(line) == True:
        continue
      elif line == 'dirs':
        temp_type = 1
      elif line == 'files':
        temp_type = 2
      elif line == 'macro':
        temp_type = 3
      else:
        if temp_type == 1:
          self.__temp_dirs.append(CreateSln.__ParseTempKeyVal(line))
        if temp_type == 2:
          self.__temp_files.append(CreateSln.__ParseTempKeyVal(line))
        elif temp_type == 3:
          self.__temp_macro.append(CreateSln.__ParseTempKeyVal(line))
    return True

  # 创建需要的目录结构
  def __CreateDirsTree(self):
    for folder in self.__temp_dirs:
      folder = folder[1]
      path = self.__sln_path + '\\' + folder
      path = os.path.abspath(path)
      if os.path.isdir(path) == False:
        try:
          os.mkdir(path)
        except OSError as error:
          self.__last_error = '创建目录失败:' + folder
          return False
    return True

  # 复制单个模板文件
  def __CopyTempFile(self, src, dst):
    # 如果存在，删掉
    if os.path.isfile(src) == False:
        self.__last_error = '复制模板--模板文件不存在:' + src
        return False
    if os.path.isfile(dst) == True:
      try:
        os.remove(dst)
      except OSError as error:
        self.__last_error = '复制模板--删除目标文件错误:' + dst
        return False
    shutil.copy(src, dst)
    return True

  # 复制模板文件
  def __CopyTempFiles(self):
    for f in self.__temp_files:
      if len(f) != 2:
        continue
      src = self.__temp_path + '\\' + f[0]
      dst = self.__sln_path + '\\' + f[1]
      dst = utility.RepTempStr(self.__temp_macro, dst)

      if self.__CopyTempFile(src, dst) == False:
        return False
      if utility.RepTempCode(self.__temp_macro, dst) == False:
        return False
    return True

  def __CopyTemp(self):
    print('开始复制模板')
    # 读取模板列表
    if self.__GetTempInfo() == False:
      return False
    
    if self.__CreateDirsTree() == False:
      return False

    if self.__CopyTempFiles() == False:
      return False
    if self.__CopyTempFiles() == False:
      return False

    return True

  #end
  ##################################################
  
  ##################################################
  # 对外接口

  # 创建项目
  def Create(self):
    if self.__SelfTest() == False:
      return False

    if self.__CopyTemp() == False:
      return False

    return True
  
  # 创建项目信息
  def CreateInfoFile(self):
    str_s = ''

    str_s += 'sln_name:' + self.__sln_name + '\r\n'
    str_s += 'namespace:' + self.__sln_namespace + '\r\n'

    path = self.__sln_path + '\\project\\project_info.txt'
    if utility.WriteFileToStr(path, str_s) == False:
      self.__last_error = '写入工程信息错误--' + utility.GetLastError()
      return False

    return True
  
  # 创建Git项目并提交一次
  def UsingGit(self):
    try:
      repo = git.Repo(self.__sln_path)
    except git.InvalidGitRepositoryError as er:
      repo = git.Repo.init(self.__sln_path)
      repo.index.add(['project', 'src', 'tools', 'make_project.bat'])
      repo.index.commit('init')
    
    # 需要手动是否，否则会出现异常
    repo.__del__()

    print('创建Git项目完成')
    return True

  # 获取最后一个错误描述
  #   每个函数返回False，都需要填写对应的错误原因
  def GetLastError(self):
    return self.__last_error
  
  # end
  ##################################################


def ParseArgs():
  parse = argparse.ArgumentParser()

  parse.add_argument('--debug', '-d', action = 'store_true', help = '调试用，使用测试输入')

  parse.add_argument('--path', '-p', help = '需要创建文件的路径')
  parse.add_argument('--name', '-n', help = '工程名')
  parse.add_argument('--namespace', '-s', help = '工程的命名空间')

  args = parse.parse_args()

  return args

def main():
  args = ParseArgs()
  if args.debug == True:
    args.path = 'D:\\tmp\\'
    args.name = 'fde_lib'
    args.namespace = 'fde'

  # 开始执行
  cl = CreateSln(args)
  if cl.Create() == False:
    print('error--' + cl.GetLastError())
    return
  
  if cl.CreateInfoFile() == False:
    print('error--' + cl.GetLastError())
    return
  
  if cl.UsingGit() == False:
    print('error--' + cl.GetLastError())
    return

  print('项目创建完成')


if __name__ == '__main__':
  main()
