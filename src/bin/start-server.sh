#!/bin/bash

CONTAINER_ROLE=${CONTAINER_ROLE}

if [ "$CONTAINER_ROLE" = "test" ]; then
  echo "$CONTAINER_ROLE"
  python manage.py test;

else
# Function to display a loader animation
  function show_loader() {
      local -r chars="/-\|"
      local -r delay=0.1
      while :; do
          for ((i=0; i<${#chars}; i++)); do
              echo -ne "\r[${chars:$i:1}] Creating Indexes... "
              sleep $delay
          done
      done
  }
  python manage.py wait_for_db
  echo -e "Running migrations -- "
  # Start the loader in the background
  show_loader &

  # Store the background process ID
  loader_pid=$!

  # Run your Python script
  indexes=$(python manage.py migrate)

  # Stop the loader when the Python script is done
  kill $loader_pid

  # Clear the loader line
  echo -e "\r\033[K"

  python manage.py runserver 0.0.0.0:8000
fi