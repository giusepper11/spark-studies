# Use a base image with Java, Python etc.
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
      openjdk-11-jdk-headless \
      python3 python3-pip curl \
      && rm -rf /var/lib/apt/lists/*

# Set Java home
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Spark version parameters
ARG SPARK_VERSION=3.5.7
ARG HADOOP_VERSION=3

ENV SPARK_HOME=/opt/spark
ENV PATH="${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"

# Create non-root user
ARG SPARK_UID=1000
ARG SPARK_GID=1000
RUN groupadd -g ${SPARK_GID} sparkgroup \
      && useradd -m -u ${SPARK_UID} -g sparkgroup -s /bin/bash sparkuser

# Download and install Spark
RUN curl -L https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
      | tar -xz -C /opt/ \
      && mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} ${SPARK_HOME}

# Create event log directory & workspace
RUN mkdir -p /opt/spark/spark-events \
      && mkdir -p /workspace \
      && chown -R sparkuser:sparkgroup /opt/spark /opt/spark/spark-events /workspace

# Copy configuration files (with correct ownership)
COPY --chown=sparkuser:sparkgroup spark/conf/spark-defaults.conf ${SPARK_HOME}/conf/

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Switch to non-root user
USER sparkuser

WORKDIR /workspace

ENTRYPOINT [ "/entrypoint.sh" ]
