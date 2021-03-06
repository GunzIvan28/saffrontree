#!/bin/bash
set -e
set -x

start_dir=$(pwd)

KMC_VERSION=3.0.0
SPADES_VERSION=3.10.1

KMC_DOWNLOAD_URL="https://github.com/refresh-bio/KMC/releases/download/v${KMC_VERSION}/KMC3.linux.tar.gz"
SPADES_URL="http://cab.spbu.ru/files/release${SPADES_VERSION}/SPAdes-${SPADES_VERSION}-Linux.tar.gz"

# Make an install location
if [ ! -d 'build' ]; then
  mkdir build
fi
cd build
build_dir=$(pwd)

# DOWNLOAD ALL THE THINGS
download () {
  url=$1
  download_location=$2

  if [ -e $download_location ]; then
    echo "Skipping download of $url, $download_location already exists"
  else
    echo "Downloading $url to $download_location"
    wget $url -O $download_location
  fi
}

# --------------- KMC ------------------
cd $build_dir
download "${KMC_DOWNLOAD_URL}" "KMC3.linux.tar.gz"
tar zxf KMC3.linux.tar.gz

# --------------- SPAdes ------------------
cd $build_dir
download $SPADES_URL "SPAdes-${SPADES_VERSION}-Linux.tar.gz"
tar zxf "SPAdes-${SPADES_VERSION}-Linux.tar.gz"
spades_dir="$build_dir/SPAdes-${SPADES_VERSION}-Linux"
cd $spades_dir

cd $start_dir

update_path () {
  new_dir=$1
  if [[ ! "$PATH" =~ (^|:)"${new_dir}"(:|$) ]]; then
    export PATH=${new_dir}:${PATH}
  fi
}

update_path ${build_dir}
update_path "${spades_dir}/bin"

pip install pyfastaq biopython==1.76 dendropy

