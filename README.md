# streaming-dumping-everything
Extract all content data for everything streaming site and download this

## Sources
**[<img src="https://avatars.githubusercontent.com/u/52610162?v=4" alt="drawing" width="64"/> Gabriel Guillou](https://github.com/Pikatsuto)**

Github Repo **[Pikatsuto/streaming-dumping-everything](https://github.com/Pikatsuto/streaming-dumping-everything)**

Docker Repo **[Pikatsuto/streaming-dumping-everything](https://hub.docker.com/r/pikatsuto/streaming-dumping-everything)**

## functionality:
### Actual
- Scan any streaming site (under development, currently configured on anime sama)
- Multi-threaded download
- automatic relaunch (currently every 2 hours)
- automatic player change in case of error
- quality filter (currently 1080p then 720p then better)
- automatic freeze detection on scraping and relaunch
- automatic language replacement (currently VO to VF)

### TODO
- add the configurations of the above options
- develop a second container to stream content found on Jellyfin without downloading it

## Docker:
### Compose
```yml
#########
services:
#########


##########################################################
  CN_Streaming_Dumping_Evrything:
    # -------------------------------------------------- #
    image: 'pikatsuto/streaming-dumping-everything:latest'
    network_mode: 'bridge'
    # -------------------------------------------------- #
    hostname: 'CN_Streaming_Dumping_Evrything'
    container_name: 'CN_Streaming_Dumping_Evrything'
    # -------------------------------------------------- #
    environment:
      ARGS: "-sd -t 6"
    # -------------------------------------------------- #
    volumes:
      - './data:/app/data'
##########################################################
```

### CLI
```bash
docker run \
    --network bridge \
    -e ARGS="-sd -t 6" \
    -v "./data:/app/data" \
    --hostname "CN_Streaming_Dumping_Evrything" \
    --name "CN_Streaming_Dumping_Evrything" \
    pikatsuto/streaming-dumping-everything:latest
```