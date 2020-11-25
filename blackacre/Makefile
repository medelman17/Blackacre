proto:
	python3 -m pip install -r requirements.txt
	python3 -m spacy download en_core_web_md
	python3 -m grpc_tools.protoc \
	    -I../server/ --python_out=. --grpc_python_out=. \
	    ../server/blackacre.proto
