# Zephyr Application

A minimal STM32MP25x Ambient zephyr firmware with an openamp remoteproc application.
The application reads a GPIO pin to determine whether it is connected to ground, and reports over rpmsg tty either 'on' or 'off'

## Features
  - Uses Zephyr RTOS
  - Builds for the `stm23mp257f_dk/stmp257fxx/m33` board by default
  - Dockerized multistage image for reproducible builds
  - Extensive debug logs and comments to assist with configuring this on other boards.
  - Uses OpenAMP and RPMSG to communicate with Linux.

## Hardware
### STM32MP25x
The zephyr application reads pin 'GPIOA_1'. 

## IMX93
The zephyr application reads pin 'GPIO_IO03' (pin 5) on the imx93). You can bridge this pin to the pin adjacent to it (pin 6) to ground it. Both pins are 3 positions down.

## Dependencies
The build is container-based; the host machine only needs the tools that
bootstrap the containerised build:

- Docker or Podman – to run the build and deploy container

## Usage

```bash
# Pre-fetch the base image
# this will save a lot of time when building as docker wont otherwise cache layers this large
podman pull zephyrprojectrtos/zephyr-build:v0.28.0

# Build container
podman build -t amcomms .
# Copy to remote
podman save amcomms | ssh root@remote 'podman load'
# Launch
ssh root@remote 'podman run -d --runtime io.containerd.remoteproc.v1 --annotation remoteproc.name=m33 amcomms'
```

## Manual testing
From the Linux side, you can check rprocmsg is working by running
```bash
cat /dev/ttyRPMSG0
```
on one terminal, and on the other terminal echo arbitrary messages to the same device
```bash
echo "arbitrary" > /dev/ttyRPMSG0
```
You will now see the on/off responses in the cat terminal when the switch's state changes.
