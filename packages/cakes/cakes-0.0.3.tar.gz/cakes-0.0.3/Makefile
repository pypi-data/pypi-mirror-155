ROOT_DIR := $(shell dirname "$(realpath $(MAKEFILE_LIST))")

.PHONY = proto clean test

proto: \
        src/cakes/proto/cakes_pb2.py \
        src/cakes/proto/cakes_pb2_grpc.py

test:
	cd $(ROOT_DIR) && \
	tox --current-env

clean:
	rm -f src/cakes/proto/cakes_pb2.py
	rm -f src/cakes/proto/cakes_pb2_grpc.py
	
src/cakes/proto/cakes_pb2.py: src/cakes/proto/cakes.proto
	python3 -m grpc_tools.protoc \
	  src/cakes/proto/cakes.proto \
	  --proto_path=src/cakes/proto \
	  --grpc_python_out=src/cakes/proto \
	  --python_out=src/cakes/proto
	sed -i 's/import cakes_pb2 as cakes__pb2/from cakes.proto import cakes_pb2 as cakes__pb2/' src/cakes/proto/cakes_pb2_grpc.py

src/cakes/proto/cakes_pb2_grpc.py: src/cakes/proto/cakes.proto
	python3 -m grpc_tools.protoc \
	  src/cakes/proto/cakes.proto \
	  --proto_path=src/cakes/proto \
	  --grpc_python_out=src/cakes/proto \
	  --python_out=src/cakes/proto
	sed -i 's/import cakes_pb2 as cakes__pb2/from cakes.proto import cakes_pb2 as cakes__pb2/' src/cakes/proto/cakes_pb2_grpc.py
