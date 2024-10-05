# Download the data from AWS 
aws s3 sync "s3://openalex/data/works" "openalex-snapshot/data/works" --no-sign-request 
# file directory
cd ~/openalex-snapshot/data/works
# Unzip .gz files
find . -name "*.gz" -exec gunzip {} \;
