# Twemproxy Docker!
This docker image contains twemproxy configured to run standalone with
two bundled memcached instances or memcached instances dynamically
looked up via EC2 instance tags. 

## Running It

```bash

docker run -d -p 22121:22121 -p 22222:22222 zapier/twemproxy

```

Now you should be able to point any run of the mill memcached client at
it on port 22121 and start using it with two bundled memcache instances

### Linking
Youc an also use this with other memcache containers via linking. For
example let's start up 3 memcache containers.

```bash
docker run --name a -d --expose 11211 tutum/memcached
docker run --name b -d --expose 11211 tutum/memcached
docker run --name c -d --expose 11211 tutum/memcached
```

Now let's link them so that they are proxied by twemproxy. The only
requirement here is that the link name MUST start with the name
"memcache" as we look for links that begin with this name and auto add
them.


```
docker run \
  --link a:memcache1 \
  --link b:memcache2 \
  --link c:memcache3 \
  -d -p 22121:22121 twemproxy 
```

You can also specify consistent node names so you can ensure the same
routing algorith regardless of IP address changes.

```
docker run \
  --link a:memcache1 \
  --link b:memcache2 \
  --link c:memcache3 \
  -e MEMCACHE1_CONSISTENT_NAME=optmius \
  -e MEMCACHE2_CONSISTENT_NAME=megatron \
  -e MEMCACHE3_CONSISTENT_NAME=starscream \
  -d -p 22121:22121 twemproxy 
```

This will generate a nutcracker configuration like the following.

```yaml
gamma:
  auto_eject_hosts: false
  distribution: ketama
  hash: fnv1a_64
  hash_tag: 'P:'
  listen: 0.0.0.0:22121
  servers:
  - 172.17.0.4:11211:1 optimus
  - 172.17.0.3:11211:1 megatron
  - 172.17.0.2:11211:1 starscream
  timeout: 250

```

### Tests

There is already a tiny test suit that runs in a docker container to test the connectivity with twemproxy. To run it, you need to run the twemproxy container:

```
sudo docker run --name nutcracker -d -p 22121:22121 -p 22222:22222 zapier/twemproxy

```

You'll also need to cd to the test directory of the repository and built the test docker image:

```
sudo docker build -t memcache_test .
```

Once that is done, you can run the test container by linking the nutcracker container.

```
sudo docker run --link nutcracker:proxy --name test --rm memcache_test

```

If all goes well, you should see some passing tests!

![](http://i.imgur.com/NqjCRIN.png)

### AWS Support

You can swap out the embedded backends for real backends on EC2 by
defining a series of environment variables to define what instances to
use as backends based on tags. 

```bash

docker run -d \
  -p 22121:22121 -p 22222:22222 \
  -e AWS_TAG_NAME=role \
  -e AWS_TAG_VALUE=cache \
  -e AWS_PUBLIC_IP=false \
  zapier/twemproxy


```

This will collect all EC2 instances tagged with role=cache and populate
the backend list with private IP addresses. 

## Building It
A token vagrant box is provided for those who do not have a native
docker environment. 

```bash
sudo docker build . # seriously were you expecting more???
```

* `generate_configs.py` - python script that generates supervisor and
twemproxy (nutcracker) configurations dynamically
* `run.sh` - shell script to run generate_configs.py followed by
supervisor. Runs by default when starting the container.

