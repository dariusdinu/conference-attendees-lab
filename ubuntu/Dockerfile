FROM ubuntu:24.04

RUN apt-get update \
  && apt-get install -y --no-install-recommends curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

CMD ["bash", "-lc", "echo 'Ubuntu debug container ready. Try: curl http://backend:8000' && sleep infinity"]