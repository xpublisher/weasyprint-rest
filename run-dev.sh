#!/usr/bin/env bash

echo "ENV: ${ENABLE_BUILD_TEST_IMAGE_UPDATE}"
if [ "${ENABLE_BUILD_TEST_IMAGE_UPDATE}" == "true" ]
then
  make test;
fi

/venv/bin/python3 -m weasyprint_rest
