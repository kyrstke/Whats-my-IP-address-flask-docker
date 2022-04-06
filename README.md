# ip-getter-python-flask-sqlite

A simple application returning client's IP addresses (public and local) as well as two lists containing IPs that have queried the app in the past.
The lists are stored in an external SQLite database, running in an individual container.
The app supports ```.html, .txt, .xml, .yaml``` and ```.json``` formats which correspond to the following MIME types respectively:

- text/html
- text/plain
- application/xml
- application/x-yaml
- application/json

The app implements rate limiting. The maximum number of requests is set to 50 per hour and 5 per minute.

## Prerequisites

[Docker](https://www.docker.com/get-docker)

## Setup

You can either run the image directly from Docker Hub or build it locally from source files.

### Docker Hub

Open Command Prompt or Terminal and run docker image:

```
docker run -dp 5000:5000 januzo/ip-getter-python-flask-sqlite
```

The command launches the app automatically after downloading the image. 

If you are using Docker Desktop you can terminate the app by pressing stop button. 
Alternatively, you can type ```docker ps``` and copy the ID of the container you want to shut down and replace PROCESS_ID with the ID:

```
docker kill PROCESS_ID
```

You can also pass the automatically generated name instead of ID. Trying to pass ```januzo/ip-getter-python-flask-sqlite``` as the name will not work.

### Local build

Open Command Prompt or Terminal in the project directory and type:

```
docker-compose up
```

To stop the image type:

```
docker-compose down
```

If you made some changes to the source code and want to rebuild the image run ```docker-compose up``` with ```--build``` option.

## Running

You can access the app from your browser by accessing http://localhost:5000/. 

You can also send requests using Postman or cURL by typing:

```
curl http://localhost:5000/ -H "Accept: text/plain"
```

The ```-H``` option stands for header. The application will send a response in the specified format.
