# Create an docker image named py-dev from the Dockerfile-dev named Dockerfile-dev
docker build -t py-api-dev -f Dockerfile-dev .

# Create a runnning container from the docker image created above and attach to it.
# The command names the container py-dev, runs interactively,
# mounts the host file system to the docker container to keep the files in sync.
# Change the paths to what is needed in your environment.
docker run --name py-api-dev -it --rm -v ~/work/bakeoff-py-api:/home/mwehby/py-api-dev --entrypoint bash py-api-dev

# If you run the container with a name, you can attach
# a second shell by running the docker exec
docker exec -i -t py-api-dev /bin/bash
