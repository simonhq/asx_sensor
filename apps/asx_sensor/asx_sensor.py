############################################################
#
# This class aims to get the ASX pricing information for the stock
#
# written to be run from AppDaemon for a HASS or HASSIO install
#
# created: 14/08/2020
#
############################################################

############################################################
#
# In the apps.yaml file you will need the following
# updated for your database path, stop ids and name of your flag
#
# asx_sensor:
#   module: asx_sensor
#   class: Get_ASX_info
#   TICKER: "CBA,TLS,BHP"
#   TICK_FLAG" "input_boolean.asx_check"
#
############################################################

# import the function libraries
import requests
import datetime
import json
import appdaemon.plugins.hass.hassapi as hass
import yfinance as yf


class Get_ASX_info(hass.Hass):

    # the name of the flag in HA (input_boolean.xxx) that will be watched/turned off

    TICKER = ""
    TICK_FLAG = ""
    URLc = "https://www.asx.com.au/asx/1/company/"
    URLs = "https://www.asx.com.au/asx/1/share/"
    URLch = "https://www.asx.com.au/asx/1/chart/highcharts?years=10&asx_code="
    SYM = ""

    s_price = "/prices?interval=daily&count=1"
    c_fields = "?fields=primary_share,latest_annual_reports,last_dividend,primary_share.indices"
    c_similar = "/similar?compare=marketcap"
    c_announcements = "/announcements?count=10&market_sensitive=false"
    c_dividends = "/dividends/history?years=1"
    c_dividends_b = "/dividends"
    c_options = "/options?count=5000"
    c_warrants = "/warrants?count=5000"
    c_people = "/people"

    tick_up_mdi = "mdi:arrow-top-right"
    tick_down_mdi = "mdi:arrow-bottom-left"
    tick_mdi = "mdi:progress-check"
    up_sensor = "sensor.asx_data_last_updated"
    asx_sensor = "sensor.asx_sensor_"
    up_mdi = "mdi:timeline-clock-outline"
    payload = {}
    headers = {"User-Agent": "Mozilla/5.0"}

    # run each step against the database
    def initialize(self):

        # get the values from the app.yaml that has the relevant personal settings
        self.TICKER = self.args["TICKER"]
        self.TICK_FLAG = self.args["TICK_FLAG"]

        # create the original sensor
        self.load()

        # listen to HA for the flag to update the sensor
        self.listen_state(self.main, self.TICK_FLAG, new="on")

        # set to run each morning at 5.17am
        runtime = datetime.time(5, 17, 0)
        self.run_daily(self.daily_load, runtime)

    # run the app
    def main(self, entity, attribute, old, new, kwargs):
        """create the sensor and turn off the flag"""
        # create the sensor with the information
        self.load()

        # turn off the flag in HA to show completion
        self.turn_off(self.TICK_FLAG)

    # run the app
    def daily_load(self, kwargs):
        """scheduled run"""
        # create the sensor with the dam information
        self.load()

    def load(self):
        """parse the ASX JSON datasets"""

        # create a sensor to keep track last time this was run
        tim = datetime.datetime.now()
        # tomorrow = tim - datetime.timedelta(days=-1)
        date_time = tim.strftime("%d/%m/%Y, %H:%M:%S")
        # date_date = tim.strftime("%d/%m/%Y")
        # tomorrow_date = tomorrow.strftime("%d/%m/%Y")
        self.set_state(
            self.up_sensor,
            state=date_time,
            replace=True,
            attributes={
                "icon": self.up_mdi,
                "friendly_name": "ASX Data last sourced",
                "Companies": self.TICKER,
            },
        )

        # split the tickers into an array
        ticks = self.TICKER.split(",")

        for tick in ticks:

            share_code = tick.strip() + ".AX"
            share = yf.Ticker(share_code)
            share_info = share.info

            current_price = float(share_info.get("currentPrice"))

            open = float(share_info.get("open"))

            if open > current_price:
                icon_mdi = self.tick_down_mdi
            elif open < current_price:
                icon_mdi = self.tick_up_mdi
            else:
                icon_mdi = self.tick_mdi

            self.set_state(
                self.asx_sensor + tick.strip(),
                state=str(share_info.get("currentPrice")),
                replace=True,
                attributes={
                    "icon": icon_mdi,
                    "open": open,
                    "friendly_name": str(share_info.get("shortName")),
                    "day_high": str(share_info.get("dayHigh")),
                    "day_low": str(share_info.get("dayLow")),
                },
            )
