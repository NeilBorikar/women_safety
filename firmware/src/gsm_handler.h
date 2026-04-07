#ifndef GSM_HANDLER_H
#define GSM_HANDLER_H

#include <Arduino.h>

class GSMHandler {
public:
    GSMHandler();
    bool init();
    bool sendAlertTrigger(float lat, float lng);
    bool sendLocationUpdate(const String& alertId, float lat, float lng);

private:
    String sendATCommand(const String& cmd, const unsigned long timeout = 2000, bool expectOk = true);
    bool initHTTP();
    bool enableNetwork();
};

#endif // GSM_HANDLER_H
