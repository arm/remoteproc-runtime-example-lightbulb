# Light-bulb example application for STM32MP25x and IMX93

This repo contains two components, a zephyr RTOS application for the M33 core, which reads the state of a GPIO pin and reports it over rpmsg tty.
And a containerised web application, that runs on the Linux side, monitoring the rpmsg tty device and displaying the state of it in a web interface.

This demonstrates a full embedded development flow using containers and [remoteproc-runtime](https://github.com/arm/remoteproc-runtime).

## Deployment

This example supports the STM32MP257x and NXP FRDM-imx93 boards
The target board must have a container engine (such as Docker), and have [remoteproc-runtime](https://github.com/arm/remoteproc-runtime) installed.

The build and deployment is fully containerised, and can be orchestrated using the [compose file](https://compose-spec.io) in the root of the project.
```sh
# set PLATFORM to either stm32mp257 or `imx93` depending on your target
PLATFORM=stm32mp257 docker compose up --build

To launch the built images, you must set the REMOTEPROC ENV var as launch time
```sh
# REMOTEPROC=`m33` for the stm32mp257x or `imx-rproc` for the FRDM-imx93
REMOTEPROC=imx-rproc docker compose up

Alternatively, services can be run independently:
See the [webapp README](./webapp/README.md) for instructions on deploying the web application side.
See the [zephyr firmware README](./zephyr-application/README.md) for instructions on building and deploying the zephyr firmware side.
