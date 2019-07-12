# Creating and Running Containers

Before we can even consider building a distributed system, we must first consider how to build the application container images that make up the pieces of our distributed system.

Container images bundle an application and its dependencies, under a root filesystem, into a single artifact. The most popular container image format is the Docker image format.

本文内容主要包括两个主题：

- How to package an application using the Docker image format
- How to start an application using the Docker container runtime

## Container Images

A container image is a binary package that encapsulates all of the files necessary to run anapplication inside of an OS container. Once the container image is present on your computer, you can run that image to produce a running application inside an OS container.

### The Docker Image Format & OCI

The Docker image format continues to be the de facto standard, and is made up of a series of filesystem layers. Each layer adds, removes, or modifies files from the preceding layer in the filesystem. This is an example of an overlay filesystem. There are a variety of different concrete implementations of such filesystems, including aufs, overlay, and overlay2.

Container images are typically combined with _a container configuration file_, which provides instructions on how to set up the container environment and execute an application entrypoint.

Containers fall into two main categories:

- System containers
- Application containers

System containers seek to _mimic virtual machines_ and often run a full boot process. They often include a set of system services typically found in a VM, such as ssh, cron, and syslog.

Application container commonly run a single application, which provides the perfect level of granularity for composing scalable applications, and is a design philosophy that is leveraged heavily by pods.

## Building Application Images with Docker

### Dockerfiles

A Dockerfile can be used to automate the creation of a Docker container image:

```
FROM alpine
MAINTAINER Kelsey Hightower <kelsey.hightower@kuar.io>
COPY bin/kuard /kuard
ENTRYPOINT ["/kuard"]
```

```bash
# bulid image
docker build -t kuard-amd64:1 .
```

### Image Secuirty

When building images that will ultimately run in a production Kubernetes cluster, be sure to follow best practices for packaging and distributing applications:

- don’t build containers with passwords baked in
- deleting a file in one layer doesn’t delete that file from preceding layers.

Secrets and images should never be mixed.

### Optimizing Image Sizes

Consider the following situation:

```
.
└── layer A: contains a large file named 'BigFile'    
    └── layer B: removes 'BigFile'        
        └── layer C: builds on B, by adding a static binary
```

Files that are removed by subsequent layers in the system are actually still present in the images; they’re just inaccessible. whenever you push or pull the image, BigFile is still transmitted through the network, even if you can no longer access it.

Another pitfall that people fall into revolves around _image caching and building_. Every time you change a layer, it changes every layer that comes after it. In general, you want to order your layers from least likely to change to most likely to change in order to optimize the image size for pushing and pulling.

### Storing Images in a Remote Registry

The standard within the Docker community is to store Docker images in a remote registry. Public registries allow anyone to download images stored in the registry, while private registries require authentication to download images.

```bash
# 给镜像打标签
docker tag kuard-amd64:1 gcr.io/kuar-demo/kuard-amd64:1
# 推送镜像
docker push gcr.io/kuar-demo/kuard-amd64:1
```

## The Docker Container Runtime

The default container runtime used by Kubernetes is Docker. Docker provides an API for creating application containers on Linux and Windows systems.

### Running Containers with Docker

To deploy a container from the gcr.io/kuar-demo/kuard-amd64:1 image, run the following command:

```bash
docker run -d --name kuard \
--publish 8080:8080 \
gcr.io/kuar-demo/kuard-amd64:1
```

kuard exposes a simple web interface:

```bash
curl http://localhost:8080
```

### Limiting Resource Usage

Docker provides the ability to limit the amount of resources used by applications by exposing the underlying _cgroup technology_ provided by the Linux kernel.

Limiting memory resources:

```bash
# stop and remove the current kuard container
docker stop kuard
docker rm kuard

# start another kuard container using the appropriate flags to limit memory usage
docker run -d --name kuard \
--publish 8080:8080 \
--memory 200m \
--memory-swap 1G \
gcr.io/kuar-demo/kuard-amd64:1
```

Limiting CPU resources:

```bash
docker run -d --name kuard \  
--publish 8080:8080 \  
--memory 200m \  
--memory-swap 1G \  
--cpu-shares 1024 \  
gcr.io/kuar-demo/kuard-amd64:1
```

### Cleanup

Once you are done building an image, you can delete it with the `docker rmi` command:

```bash
docker rmi tag-name
# or
docker rmi image-id
```

Unless you explicitly delete an image it will live on your system forever, even if you build a new image with an identical name.

## summary

Application containers provide a clean abstraction for applications, and when packaged in the Docker image format, applications become easy to build, deploy, and distribute.
