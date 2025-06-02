#!/bin/bash

# This script sets up proper Docker permissions for the SQL Practice feature

# Check if Docker socket group exists and user has access
if [ -S /var/run/docker.sock ]; then
  echo "Docker socket exists"
  
  # Get the group of the docker socket
  DOCKER_GROUP=$(stat -c '%G' /var/run/docker.sock)
  
  if [ "$DOCKER_GROUP" = "UNKNOWN" ]; then
    # If group is unknown, get the GID
    DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)
    echo "Docker socket belongs to GID $DOCKER_GID"
    
    # Check if a group with this GID already exists
    if getent group $DOCKER_GID > /dev/null; then
      DOCKER_GROUP=$(getent group $DOCKER_GID | cut -d: -f1)
      echo "Group $DOCKER_GROUP already exists for GID $DOCKER_GID"
    else
      # Create a new docker group with the correct GID
      sudo groupadd -g $DOCKER_GID docker_alt
      DOCKER_GROUP="docker_alt"
      echo "Created new group $DOCKER_GROUP with GID $DOCKER_GID"
    fi
  else
    echo "Docker socket belongs to group $DOCKER_GROUP"
  fi
  
  # Add current user to the docker group
  if ! groups | grep -q "\b$DOCKER_GROUP\b"; then
    echo "Adding user $(whoami) to group $DOCKER_GROUP"
    sudo usermod -aG $DOCKER_GROUP $(whoami)
    echo "Please log out and log back in for the group changes to take effect"
    echo "Alternatively, run: newgrp $DOCKER_GROUP"
  else
    echo "User $(whoami) is already in group $DOCKER_GROUP"
  fi
  
else
  echo "Docker socket not found at /var/run/docker.sock"
  echo "Please make sure Docker is installed and running"
  exit 1
fi

# Test Docker connectivity
echo "Testing Docker connectivity..."
docker info > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "Docker is working correctly!"
else
  echo "Cannot connect to Docker daemon. Make sure Docker is running or restart your session."
  exit 1
fi
