# Use the official MinIO image as the base image
FROM quay.io/minio/minio

# Expose the default MinIO port and console port
EXPOSE 9000
EXPOSE 9001

# Create a data folder and set permissions for MinIO to store objects
RUN mkdir -p /data && chmod 777 /data

# Set the entrypoint for running the MinIO server with console address
CMD ["server", "/data", "--console-address", ":9001"]
