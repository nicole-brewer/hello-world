# Docker Continued



## What `localhost` means in a docker container

Let's say I wrote a program that work on my desktop by refering to `localhost` and I want to run that program in a container without major modification. I can use the `--network="host"` in my `docker run` command, then use `127.0.0.1` to refer to localhost. But this doesn't really work when you start getting into publishing ports. In other words, in docker containers, we still consider our coding perspective to be the admin running the container on another machine (as opposed to thinking about networking relative to the container).



## Building Dockerfiles well

- Every time you change a file in docker, both versions of the file live on in the image. To prevent many copies for mulitiple edits, make all changes to a file with a double ampersand.
- When we add a package from a base image that has apt-get installed,  we have to put the `apt-get update -y && apt-get <package-name>` because apt-get is a part of the previous build cache and must be added to the new cache by making the update.



## Clean up

```bash
# remove dangling images
docker system prune
# and also any stopped containers and unused images
docker system prune -a

docker volume prune
```



## An alternative to `docker system prune`

```
# Stop all containers you want to delete
docker stop $(docker ps -a -q --filter ancestor="<image-name>")
# Delete all containers you want to delete
docker rm $(docker ps -a -q --filter ancestor="<image-name>")
# Delete all untagged images
docker rmi $(docker images -q --filter "dangling=true")


# Delete all images
docker rmi $(docker images -q)
```



##Save file from container to host

```pwd
docker cp <containerId>:/file/path/within/container /host/path/target
```