# 文档转换器

cots.libs.logger 基于ES的可以自定义的日志库

## 目录结构

```
├── docs                           # 文档
├── logger                         # 源码
├── tests                       # 测试示例文件
```

## 发布

```
# 生成依赖清单
pip freeze > requirements.txt

# 根据依赖清单安装环境
pip install -r requirements.txt


# 打包环境安装
python -m pip install setuptools wheel twine
pip install --user --upgrade setuptools wheel

# 本地安装
python setup.py install

# 构建输出
python setup.py sdist bdist_wheel

#上传包
twine upload --username Admin --password Admin --repository-url http://nuget.cityocean.com/pypi/COMS-Pypi/legacy dist/*

```
