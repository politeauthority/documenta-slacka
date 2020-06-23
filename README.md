# Documenta Slacka


## Development

To build the container.
```console
docker build . -t="documeta-slacka:dev" -f dev.Dockerfile
```

To run the container.
```
docker run \
    --name documenta-slacka-dev \
    -v /Users/alixfullerton/repos/personal/documenta-slacka/src:/app \
    -p 5000:5000 \
    -e SLACK_API_TOKEN=TOKEN \
    -d \
    --rm \
    documeta-slacka:dev
```
