#!/bin/bash

download_link=https://github.com/ArjunSahlot/password_manager/archive/main.zip
temporary_dir=$(mktemp -d) \
&& curl -LO $download_link \
&& unzip -d $temporary_dir main.zip \
&& rm -rf main.zip \
&& mv $temporary_dir/password_manager-main $1/password_manager \
&& rm -rf $temporary_dir
echo -e "[0;32mSuccessfully downloaded to $1/password_manager[0m"
