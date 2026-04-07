#include "gps_handler.h"
#include <HardwareSerial.h>
#include <TinyGPS++.h>
#include "config.h"

HardwareSerial GPSSerial(2); // Use UART2
TinyGPSPlus gps;

GPSHandler::GPSHandler() {
    lastLat = 0.0;
    lastLng = 0.0;
    hasValidData = false;
}

void GPSHandler::init() {
    GPSSerial.begin(GPS_BAUDRATE, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);
    Serial.println("GPS UART Initialized.");
}

void GPSHandler::update() {
    while (GPSSerial.available() > 0) {
        gps.encode(GPSSerial.read());
    }

    if (gps.location.isUpdated()) {
        lastLat = gps.location.lat();
        lastLng = gps.location.lng();
        hasValidData = true;
    }
}

GPSData GPSHandler::getLatestData() {
    GPSData data;
    data.latitude = lastLat;
    data.longitude = lastLng;
    data.isValid = hasValidData;
    return data;
}
