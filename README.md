# feather-th-azure-iot
 An internet-connected temperature and humidity monitor for 3D printer enclosures based on the [Adafruit Feather TFT ESP32-S3](https://www.adafruit.com/product/5483) board and [AHT20 breakout sensor](https://www.adafruit.com/product/4566). 
 
 Code will be written in CircuitPython, and cloud functionality will run through Microsoft Azure, with an emphasis on their low- and no-cost service tiers.

I created this project both to learn more about CircuitPython as well as Azure's IOT services. (Disclosure: I work for Microsoft, but this project is in no way sponsored or endorsed by the company.)

Feature planning & roadmaps will be maintained in this repo's Issues.

# Requirements

* Firmware: [CircuitPython v8.x for ESP32-S3 TFT PSRAM](https://circuitpython.org/board/adafruit_feather_esp32s3_tft/)
* Python Libraries:
    * [Adafruit CircuitPython library bundle for v8.x](https://circuitpython.org/libraries) (currently in alpha)
    * [Adafruit_CircuitPython_AzureIoT library](https://docs.circuitpython.org/projects/azureiot/en/latest/)

