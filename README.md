# Light-bulb example application for STM32MP25x and IMX93

This repo contains two components, a zephyr RTOS application for the M33 core, which reads the state of a GPIO pin and reports it over rpmsg tty.
And a containerised web application, that runs on the Linux side, monitoring the rpmsg tty device and displaying the state of it in a web interface.

This demonstrates a full embedded development flow using containers and [remoteproc-runtime](https://github.com/arm/remoteproc-runtime).

## Deployment

This example supports the STM32MP257x and NXP FRDM-imx93 boards
The target board must have a container engine (such as Docker), and have [remoteproc-runtime](https://github.com/arm/remoteproc-runtime) installed.

The build and deployment is fully containerised, and can be orchestrated using the [compose file](https://compose-spec.io) in the root of the project.

We recommend pre-fetching the base image - this will save a lot of time when building as docker won't otherwise cache layers this large:

```sh
docker pull zephyrprojectrtos/ci-base:v0.28.0
```

To build the image on your development machine, run:
```sh
# set PLATFORM to either stm32mp257 or `imx93` depending on your target
PLATFORM=stm32mp257 docker compose build
```

To transfer the images to your target board, run:
```sh
docker save remoteproc-runtime-example-lightbulb-webapp:latest | ssh root@remote 'docker load'
docker save remoteproc-runtime-example-lightbulb-zephyr:latest | ssh root@remote 'docker load'
```

To launch the built images on the target board, run the containers directly:
```sh
# Start the zephyr firmware (use m33 for STM32MP257x or imx-rproc for FRDM-imx93)
ssh root@remote 'docker run -d --name remoteproc-zephyr --runtime=io.containerd.remoteproc.v1 --annotation remoteproc.name=m33 remoteproc-runtime-example-lightbulb-zephyr:latest'

# Start the webapp
ssh root@remote 'docker run -d --name remoteproc-webapp --privileged -p 3000:3000 -v /dev:/dev -e SECRET_KEY=change-me-in-production --restart=on-failure remoteproc-runtime-example-lightbulb-webapp:latest'
```

The web interface will be available at `http://<target-ip>:3000`

Alternatively, services can be run independently:
See the [webapp README](./webapp/README.md) for instructions on deploying the web application side.
See the [zephyr firmware README](./zephyr-application/README.md) for instructions on building and deploying the zephyr firmware side.
