#!/bin/bash

PKGNAME="Mac Set Default Apps"
VERSION="1.0.0"
INSTALL_DIR="/usr/local/bin/"
IDENTIFIER="com.dgrdev.msda"

export PATH=/usr/bin:/bin:/usr/sbin:/sbin

project_folder=$(dirname "$0")

find "${project_folder}/payload" -type f -exec chmod 755 {} \;

pkgbuild --root "${project_folder}/payload" \
	--identifier "${IDENTIFIER}" \
	--version "${VERSION}" \
	--install-location "${INSTALL_DIR}" \
	--filter='*.py'\
	--filter='*.pyc'\
	"${project_folder}/${PKGNAME} v${VERSION}.pkg"
