# TP04: Containerization and Big Data Environment Deployment

## Project

This project analyzes a CSV dataset inside a Docker container. It reports the number of rows, average score, and count per category.

## Files

- `app.py`: CSV processing application.
- `data/dataset.csv`: sample TP03-style dataset.
- `Dockerfile`: custom Python image definition.
- `compose.yaml`: reproducible Compose environment.
- `screenshots/`: execution evidence.

## Task 1: Installation

```bash
docker --version
docker compose version
```

Create a Docker Hub account at https://hub.docker.com/.

## Task 2: Image

Replace `YOUR_DOCKERHUB_USERNAME` with the Docker Hub username:

```bash
docker build -t YOUR_DOCKERHUB_USERNAME/tp04-analysis:1.0 .
docker login
docker push YOUR_DOCKERHUB_USERNAME/tp04-analysis:1.0
docker pull YOUR_DOCKERHUB_USERNAME/tp04-analysis:1.0
```

## Task 3: Containers and network

```bash
docker network create tp04-network
docker run -d --name tp04-1 --network tp04-network YOUR_DOCKERHUB_USERNAME/tp04-analysis:1.0
docker run -d --name tp04-2 --network tp04-network YOUR_DOCKERHUB_USERNAME/tp04-analysis:1.0
docker run -d --name tp04-3 --network tp04-network YOUR_DOCKERHUB_USERNAME/tp04-analysis:1.0
docker ps
docker network inspect tp04-network
docker logs tp04-1
docker stop tp04-1 tp04-2 tp04-3
docker rm tp04-1 tp04-2 tp04-3
docker network rm tp04-network
```

For port mapping, use `-p 8081:8000`, `-p 8082:8000`, and `-p 8083:8000` when the application exposes a service. This batch application does not listen on a port, so port mapping is not needed for its output.

## Task 4: Docker Compose

```bash
docker compose up --build
docker compose ps -a
docker compose down
```

Docker Compose solves the problem of managing a multi-container application with one declarative file. It stores services, networks, volumes, names, and startup settings together.

`docker run` starts one container with options supplied on the command line. `docker compose up` reads `compose.yaml`, builds images when needed, and starts the complete application environment consistently.

A database can be added as another service:

```yaml
  database:
    image: postgres:16
    environment:
      POSTGRES_DB: analysis
      POSTGRES_USER: analyst
      POSTGRES_PASSWORD: analyst
    volumes:
      - database-data:/var/lib/postgresql/data

volumes:
  database-data:
```

The analysis service could then connect to the hostname `database`.

## Task 5: Report

Docker packages an application and its dependencies into an isolated, portable environment. This is useful in data science because the same Python version, libraries, files, and commands can be used on every machine.

An image is an immutable template containing the application and its dependencies. A container is a running, isolated instance created from an image.

In the Dockerfile, `FROM` selects the base image, `WORKDIR` sets the working directory, `COPY` puts project files into the image, `RUN` executes build-time commands, and `CMD` defines the default command executed when the container starts.

## Evidence

The included screenshot records the successful Compose build and application output. Run the commands above again to reproduce it.
