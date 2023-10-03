.PHONY: run test clean
IMAGE=eforth.dec
BITS=16

run test: subleq.py ${IMAGE}
	./subleq.py ${BITS} ${IMAGE}

clean:

