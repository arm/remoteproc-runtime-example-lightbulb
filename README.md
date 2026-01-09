# Light-bulb example application for STM32MP25x and IMX93

This repo contains two components, a zephyr RTOS application for the M33 core, which reads the state of a GPIO pin and reports it over rpmsg tty.
And a containerised web application, that runs on the Linux side, monitoring the rpmsg tty device and displaying the state of it in a web interface.

This demonstrates a full embedded development flow using containers and [remoteproc-runtime](https://github.com/arm/remoteproc-runtime).

## Deployment

This example fully supports the STM32MP257x boards, and the FRDM-imx93 board. T
The build and deployment is fully containerised and can be built with
`PLATFORM=stm32mp257 docker compose up --build` and then run with [remoteproc-runtime](https://github.com/arm/remoteproc-runtime)
Where PLATFORM can equal either stm32mp257 or `imx93`, the two supported boards.

When deploying with remoteproc-runtime, the REMOTEPROC environment variable needs to be set to either
`REMOTEPROC=m33` for the stm32mp257x or
`REMOTEPROC=imx-rproc` for the FRDM-imx93

Alternatively, services can be run independently:
See the [webapp README](./webapp/README.md) for instructions on deploying the web application side.
See the [zephyr firmware README](./zephyr-application/README.md) for instructions on building and deploying the zephyr firmware side.
