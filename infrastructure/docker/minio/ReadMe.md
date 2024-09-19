# MinIO Docker Setup

Quick guide to building and running a MinIO instance using Docker.

1. ### Create the .env file:
   Create a .env file with your MinIO credentials. </br>
   Ensure the password is at least 8 characters long. </br>
   Example .env file: </br>
   ```
   MINIO_ROOT_USER=minioadmin
   MINIO_ROOT_PASSWORD=yourstrongpassword
   ```
2. ### Build the Docker Image:
   ``` bash
   docker build -t minio-instance .
   ```
3. ### Run the container:
   ``` bash
   docker run -d \
   -p 9000:9000 \
   -p 9001:9001 \
   --name minio \
   --env-file .env \
   -v ~/minio/data:/data \
   minio-instance
   ```
   - Ports 9000 and 9001 are for MinIO API and console.
   - Data is stored in ~/minio/data.

4. ### Access MinIO:
   Open the MinIO console at:
   `http://localhost:9001`

5. ### Manage the Container:
   - Stop: `docker stop minio`
   - Start: `docker start minio`
   - Remove: `docker rm -f minio`
   