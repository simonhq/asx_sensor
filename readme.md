# Australian Securities Exchange Sensor
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

_Creates sensors for Home Assistant for each ASX Symbol you provide_


## Lovelace Examples

![Example of the entities in Lovelace](https://github.com/simonhq/asx_sensor/blob/master/asx_sensor_entities.PNG)

![An Entity has 10 days information](https://github.com/simonhq/asx_sensor/blob/master/asx_sensor_entity.PNG)

## Installation

This app is best installed using [HACS](https://github.com/custom-components/hacs), so that you can easily track and download updates.

Alternatively, you can download the `asx_sensor` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `asx_sensor` module.

## How it works

The [ASX](https://www.asx.com.au/) site provides this information in JSON format, this just makes the information available as sensors in HA.

As this is non time critical sensor, it only gets the information on a set time schedule, once per day at 7.27pm after the close of the market. 

### To Run

You will need to create an input_boolean entity to watch for when to update the sensor. When this `input_boolean` is turned on, whether manually or by another automation you create, the scraping process will be run to create/update the sensor.

## AppDaemon Libraries

Please add the following packages to your appdaemon 4 configuration on the supervisor page of the add-on.

``` yaml
system_packages: []
python_packages: []
init_commands: []
```

No specific packages are required for this app.

## App configuration

In the apps.yaml file in the appdaemon/apps directory - 

```yaml
asx_sensor:
  module: asx_sensor
  class: Get_ASX_info
  TICKER: "CBA,TLS,BHP"
  TICK_FLAG: "input_boolean.check_asx_info"
```

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | `act_garbage`
`class` | False | string | | `Get_ACT_Garbage`
`TICKER` | False | string | | The comma separated symbols for each of the stocks you are interested in
`TICK_FLAG` | False | string | | The name of the flag in HA for triggering this sensor update - e.g. input_boolean.check_asx_info

## Sensors Created

This version will create a sensor for each stock you provide

* sensor.asx_sensor_XXX

## Issues/Feature Requests

Please log any issues or feature requests in this GitHub repository for me to review.