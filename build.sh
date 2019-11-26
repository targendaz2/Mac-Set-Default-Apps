#!/bin/bash

PKGNAME="MacSetDefaultApps"
VERSION=$(./payload/msda --version 2>&1)
INSTALL_DIR="/usr/local/bin/"
IDENTIFIER="com.dgrdev.msda"

export PATH=/usr/bin:/bin:/usr/sbin:/sbin

project_folder=$(dirname "$0")

find "${project_folder}/payload" -type f \( ! -iname "*.pyc" \) -exec chmod 755 {} \;

pkgbuild --root "${project_folder}/payload" \
	--identifier "${IDENTIFIER}" \
	--version "${VERSION}" \
	--install-location "${INSTALL_DIR}" \
	--filter='.+c' \
	--filter='.+\.pyc' \
	"${project_folder}/${PKGNAME}-v${VERSION}.pkg"

exit 0
