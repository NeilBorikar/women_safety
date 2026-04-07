#ifndef GPS_HANDLER_H
#define GPS_HANDLER_H

#include <Arduino.h>

struct GPSData {
    float latitude;
    float longitude;
    bool isValid;
};

class GPSHandler {
public:
    GPSHandler();
    void init();
    void update();
    GPSData getLatestData();

private:
    float lastLat;
    float lastLng;
    bool hasValidData;
};

#endif // GPS_HANDLER_H
