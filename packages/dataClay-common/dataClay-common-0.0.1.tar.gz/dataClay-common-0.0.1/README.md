## dataClay common

- protos: common grpc protocol buffers for dataclay

#### Protos

- Compile in javaclay

```
mvn protobuf:compile-custom -Pprotogen
```
to create just grpc-stubs or
```
mvn clean compile -Pprotogen
```
to compile all javaclay including new protos
- Compile in pyclay

```
pip install grpcio-tools protobufferize
python setup.py protobufferize
```

**NOTE**: if protbufferize cannot be installed via pip, please clone
it from https://github.com/bsc-dom/protobufferize and run `python setup.py install`

# Packaging Python

python3 -m pip install --upgrade build

python3 -m build

python3 -m pip install --upgrade twine

python3 -m twine upload --repository testpypi dist/*