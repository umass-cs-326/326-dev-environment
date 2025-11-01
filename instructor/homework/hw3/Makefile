# Makefile for Gradescope Autograder

###### UTILITIES ##########################################
#
# Utility stuff to help with the rest of the Makefile.

### Generate Deterministic Obfuscated Names ###############
#
# The following is used to generate obfuscated names. We 
# are using this here to hide the docker image name that is
# generated to make it difficult for curious students to
# find the image.

# Detect OS
UNAME_S := $(shell uname -s)

# Pick sha256 tool
ifeq ($(UNAME_S),Darwin)
  SHA256 := shasum -a 256
else
  SHA256 := sha256sum
endif

### Generate Deterministic Obfuscated Names ###############

###########################################################

# List of files to include in student distribution
DIST = student/requirements.txt
SOLN = solution/requirements.txt \
	solution/main.py \
	solution/models.py

HOMEWORK_DIR := $(notdir $(CURDIR))
HOMEWORK_IMAGE_NAME = 326-${HOMEWORK_DIR}-gradescope

# Variables
DOCKER_DIR = autograder
DOCKER_USERNAME = timdrichards
#IMAGE_NAME := $(call OBF,${HOMEWORK_IMAGE_NAME})
IMAGE_NAME := $(shell printf '%s' "$(HOMEWORK_IMAGE_NAME)" | $(SHA256) | awk '{print $$1}')
TAG = latest
FULL_IMAGE = $(DOCKER_USERNAME)/$(IMAGE_NAME):$(TAG)
SAMPLE_SUBMISSION = $(CURDIR)/sample/submission
RESULTS_DIR = $(CURDIR)/sample/results

.PHONY: all build test testit push deploy clean clean-results clean-all help dist clean-dist

# Show help
help:
	@echo "Available targets:"
	@echo "  make build          - Build the Docker image"
	@echo "  make gdist          - Make Gradescope distribution"
	@echo "  make dist           - Make student distribution"
	@echo "  make test           - Test the image locally with sample submission"
	@echo "  make testit         - Test the image locally with sample submission interactively"
	@echo "  make push           - Push the image to Docker Hub"
	@echo "  make deploy         - Build and push in one command"
	@echo "  make dist           - Make student distribution zip file"
	@echo "  make clean-dist.    - Remove dist folder"
	@echo "  make clean          - Remove local Docker image"
	@echo "  make clean-results  - Remove test results"
	@echo "  make clean-all      - Remove images and results"
	@echo "  make help           - Show this help message"

# Default target
all: build

# Build the Docker image
build:
	@echo "Building Docker image: $(FULL_IMAGE)"
	cd ${DOCKER_DIR} && docker build -t $(FULL_IMAGE) .
	@echo "Build complete!"

# Test the image locally with a sample submission
test:
	@echo "Testing Docker image locally..."
	@mkdir -p $(RESULTS_DIR)
	docker run --rm \
		-v $(SAMPLE_SUBMISSION):/autograder/submission \
		-v $(RESULTS_DIR):/autograder/results \
		$(FULL_IMAGE) \
		/autograder/run_autograder
	@echo "Test complete! Results:"
	@cat $(RESULTS_DIR)/results.json

testit:
	@echo "Testing Docker image locally..."
	@mkdir -p ${RESULTS_DIR}
	docker run --rm -it \
		-v $(SAMPLE_SUBMISSION):/autograder/submission \
		-v $(RESULTS_DIR):/autograder/results \
		$(FULL_IMAGE) bash

# Push the image to Docker Hub
push:
	@echo "Pushing Docker image to Docker Hub: $(FULL_IMAGE)"
	docker push $(FULL_IMAGE)
	@echo "Push complete!"

# Build and push in one command
deploy: build push
	@echo "Deployment complete!"

# Make student distribution
dist:
	mkdir -p dist/${HOMEWORK_DIR}
	cp ${DIST} dist/${HOMEWORK_DIR}
	cd dist && zip -r ${HOMEWORK_DIR}.zip ${HOMEWORK_DIR}
	rm -rf dist/${HOMEWORK_DIR}
	
# Make solution distribution
dist-solution:
	mkdir -p dist/${HOMEWORK_DIR}
	cp ${SOLN} dist/${HOMEWORK_DIR}
	cd dist && zip -r ${HOMEWORK_DIR}-solution.zip ${HOMEWORK_DIR}
	rm -rf dist/${HOMEWORK_DIR}

clean-dist:
	@echo "Clearning distribution"
	rm -rf dist

# Clean up local Docker images
clean:
	@echo "Removing local Docker image: $(FULL_IMAGE)"
	docker rmi $(FULL_IMAGE) || true
	@echo "Cleanup complete!"

# Remove test results
clean-results:
	@echo "Removing test results..."
	rm -rf $(RESULTS_DIR)
	@echo "Results cleaned!"

# Full clean (images and results)
clean-all: clean-dist clean clean-results
