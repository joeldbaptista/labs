# Use the official Debian base image
FROM debian:latest

# Install necessary packages
RUN apt-get update && \
    apt-get install -y vim tmux sudo wget unzip && \
    apt-get clean

# Add a user with the user id 1000
ARG USERNAME
RUN useradd -m -s /bin/bash $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Add duckdb
RUN wget https://github.com/duckdb/duckdb/releases/download/v1.1.0/duckdb_cli-linux-amd64.zip && \
    unzip duckdb_cli-linux-amd64.zip && \
    mv duckdb /usr/local/bin/ && \
    chmod a+x /usr/local/bin/duckdb

# Ensure the user owns the .bashrc file
#RUN chown $USERNAME:$USERNAME /home/$USERNAME/.bashrc

# Set up password for the user
ARG PASSWORD
RUN echo "$USERNAME:$PASSWORD" | chpasswd

# Switch to the new user
WORKDIR /home/$USERNAME
USER $USERNAME

# Set default shell session to tmux
CMD [ "tail", "-f", "/dev/null" ]
