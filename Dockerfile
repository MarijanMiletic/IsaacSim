# Use the official NVIDIA Isaac Sim image as base
FROM nvcr.io/nvidia/isaac-sim:4.5.0

# Set environment variables for non-interactive installs
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install additional dependencies
COPY requirements.txt .
RUN ./python.sh -m pip install --no-cache-dir -r requirements.txt

# Copy your simulation scripts into the container
COPY . .

# Default command: run the pick and place example
# Note: ./python.sh is the wrapper provided by Isaac Sim inside the container
CMD ["./python.sh", "franka_pick_and_place.py"]
