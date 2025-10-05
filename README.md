# spark-studies

Local Docker-based Spark playground with a small WordCount example.

## What this repo contains

- A minimal Spark cluster setup using Docker:
  - [Dockerfile](Dockerfile)
  - [docker-compose.yml](docker-compose.yml)
  - [entrypoint.sh](entrypoint.sh)
- A simple word count job: [workspace/scripts/wordcount.py](workspace/scripts/wordcount.py)
- Sample input: [workspace/data/sample.txt](workspace/data/sample.txt)
- Spark defaults: [spark/conf/spark-defaults.conf](spark/conf/spark-defaults.conf)
- Helper commands in the [Makefile](Makefile)

## Requirements

- Docker & Docker Compose
- (Local dev) Python 3.10+ and pip for testing the script: `pip install -r requirements.txt`

## Quick start (Docker)

1. Build images:

   ```bash
   make build
   ```

2. Start the cluster:

   ```bash
   make up
   ```

3. Check logs:

   ```bash
   make logs
   ```

Spark master UI: <http://localhost:8080>  
History server: <http://localhost:18080>

To open a shell in the master container:

```bash
make shell
```

## Run the WordCount example

From your host (after `make up`) run spark-submit inside the master container. The repository mounts `./workspace` to `/workspace` inside containers, so use paths under `/workspace`:

```bash
docker exec -it spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /workspace/scripts/wordcount.py \
  --input_path /workspace/data/sample.txt \
  --output_path /workspace/output \
  --format parquet
```

Output will be written to `./workspace/output` on the host (or `/workspace/output` inside the container). For CSV use `--format csv`.

## Run locally without Docker

1. Create a virtualenv and install requirements:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the script with a local Spark (or pip-installed pyspark) using paths to local files:

   ```bash
   python workspace/scripts/wordcount.py --input_path workspace/data/sample.txt --output_path workspace/output --format parquet
   ```

## Useful files

- [Makefile](Makefile) — dev commands (build/up/down/logs/shell)
- [Dockerfile](Dockerfile) — image used for master/worker/history
- [docker-compose.yml](docker-compose.yml) — services & ports
- [entrypoint.sh](entrypoint.sh) — container entrypoint mode handler
- [workspace/scripts/wordcount.py](workspace/scripts/wordcount.py) — example Spark job

## Troubleshooting

- If workers cannot register, confirm `spark-master` hostname/resolution and that containers are on the same network (docker compose handles this).
- If permissions prevent writing event logs, ensure the `spark-events` volume is writable by Spark user (compose already sets this up).
- Check Spark logs in container: `docker exec -it spark-master /bin/bash` then `ls ${SPARK_HOME}/logs` and view files.

## License

MIT — adapt and reuse for study purposes.
