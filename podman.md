# CloudFlare hacking
This now requires a pupflare container to proxy for CloudFlare, and the `anime.py`
container needs to have visibility to port 3000 on the `pupflare` container.

If using podman, you can start the pupflare in a new pod like so:
```
podman pull quay.io/unixfox/pupflare
podman run -d -p 3000:3000 --pod new:mypod quay.io/unixfox/pupflare:latest
```

Then, you can run your anime.py pod like so:
```
podman run --interactive --pod mypod --tty -v <host dir>:/home:z anime-py update
```

# running on linux box
```
#!/bin/bash
podman pull quay.io/unixfox/pupflare
podman run -d -p 3000:3000 --pod new:mypod quay.io/unixfox/pupflare:latest
podman run --interactive --pod mypod --tty -v /service/anime/:/home:z anime-py update
```

# clean on linux box
```
#!/bin/bash
podman pod stop mypod
podman system prune -f
podman pod prune -f
podman container prune -f
podman image prune -f
podman rmi $(podman images -qa) -f

docker build -t anime-py .
```
