# Light-bulb example application for STM32MP25x

This repo contains two components, a zephyr RTOS application for the M33 core, which reads the state of a GPIO pin and reports it over rpmsg tty.
And a containerised web application, that runs on the Linux side, monitoring the rpmsg tty device and displaying the state of it in a web interface.

This demonstrates a full embedded development flow using containers and [remoteproc-runtime](https://github.com/arm/remoteproc-runtime).

## Deployment

This example is fully containerised and can be build with
`docker compose up --build` and then run with [remoteproc-runtime](https://github.com/arm/remoteproc-runtime)

Alternatively, services can be run independently:
See the [webapp README](./webapp/README.md) for instructions on deploying the web application side.
See the [zephyr firmware README](./zephyr/README.md) for instructions on building and deploying the zephyr firmware side.
