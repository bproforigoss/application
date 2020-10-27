# Only for documentation purposes, won't matter after containerization
EVENTSTORE_STREAM_URL = "http://127.0.0.1:2113/streams"
DOCKER_RUN_COMMAND "docker run --name eventstore-node -it -p 2113:2113 -p 1113:1113 eventstore/eventstore --insecure --enable-atom-pub-over-http"
