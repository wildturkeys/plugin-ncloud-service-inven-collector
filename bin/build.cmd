set VERSION="v0.0.10-dev"
cd ..
docker build -t ncloud-resource-explorer:%VERSION% . --no-cache
docker tag ncloud-resource-explorer:%VERSION% finalck/ncloud-resource-explorer:%VERSION%
docker push finalck/ncloud-resource-explorer:%VERSION%
cd bin

