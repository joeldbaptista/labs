# Use the official Alpine base image
FROM alpine:latest

# Install tmux, vim, doas, and other utilities
RUN apk update && \
    apk add --no-cache tmux vim doas shadow

RUN addgroup doas

# Add a user with the name provided via an environment variable
ARG USERNAME
ARG PASSWORD

RUN adduser -D -s /bin/sh $USERNAME && \
    echo "$USERNAME:$PASSWORD" | chpasswd && \
    adduser $USERNAME doas && \
    echo "permit :doas" > /etc/doas.d/doas.conf && \
    chmod 0400 /etc/doas.d/doas.conf

WORKDIR /home/$USERNAME
USER $USERNAME

CMD [ "tail", "-f", "/dev/null" ]

