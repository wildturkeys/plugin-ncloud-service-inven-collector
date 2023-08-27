cd ..

set /P VERSION=< "./spaceone/VERSION"

docker build -t ncloud-resource-explorer:%VERSION% . --no-cache
docker tag ncloud-resource-explorer:%VERSION% finalck/ncloud-resource-explorer:%VERSION%
docker push finalck/ncloud-resource-explorer:%VERSION%


