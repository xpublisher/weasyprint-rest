#!/usr/bin/env bash
echo "GOT $ENABLE_RUNTIME_TEST_ONLY"
if [ "${ENABLE_BUILD_TEST_IMAGE_UPDATE}" == "true" ] || [ "${ENABLE_RUNTIME_TEST_ONLY}" == "true" ]
then
  make test;
fi

if [ "${ENABLE_RUNTIME_TEST_ONLY}" != "true" ]
then

  /venv/bin/python3 -m weasyprint_rest
fi
