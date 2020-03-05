# Running a RabbitMQ Server on a Docker container that is mapped to localhost

```bash
# Run a rabbitqm container called 'rabbitmq'
# We use the rabbitmq:3-management image because it lets us use the management UI
# We map the containers ports to our localhost ports
# 15672 is for the UI and 5672 is for backend communication
# You can use -d for detached mode, but I like to see the info messages printed by the server
# We use --rm to remove the container automatically when we're done using it
docker run -it --rm --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3-management

# If you haven't used detached mode, open up a new buffer or tab
# Start up the message receiver, and watch messages print to stdout as they are received
# This program can be ended with <CTRL>-C
python receive.py

# Open up a new tab or buffer and start sending messages!
python send.py

```

