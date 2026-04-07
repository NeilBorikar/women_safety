#include <Arduino.h>
#include "config.h"
#include "gps_handler.h"
#include "gsm_handler.h"
#include "button_handler.h"

GPSHandler gpsHandler;
GSMHandler gsmHandler;
ButtonHandler buttonHandler;

// State tracking
bool alertIsActive = false;
unsigned long lastLocationUpdate = 0;
String currentAlertId = "DUMMY_ALERT_ID_UPDATE_VIA_RESPONSE"; // In a real app we parse from trigger response

void setup() {
    Serial.begin(115200);
    delay(1000); // Wait for Serial to initialize

    Serial.println("=====================================");
    Serial.println("Starting Women Safety ESP32 Firmware");
    Serial.println("=====================================");

    // Initialize handlers
    buttonHandler.init();
    gpsHandler.init();
    
    if (!gsmHandler.init()) {
        Serial.println("Warning: GSM Initialization Failed or Network Not Attached yet.");
    }
}

void readBatteryLevel() {
    int adcVal = analogRead(BATTERY_ADC_PIN);
    float voltage = (adcVal / 4095.0) * 3.3 * 2; // Assuming a 1/2 voltage divider
    Serial.print("Battery Voltage: ");
    Serial.print(voltage);
    Serial.println("V");
}

void loop() {
    // 1. Always update peripheral states
    gpsHandler.update();
    buttonHandler.update();

    // 2. Check SOS button state
    if (buttonHandler.isSOSActivated() && !alertIsActive) {
        Serial.println(">>> SOS TRIGGERED! <<<<");
        GPSData gpsData = gpsHandler.getLatestData();
        
        // Ensure we send something even if GPS is invalid (could use last known or 0)
        float lat = gpsData.isValid ? gpsData.latitude : 0.0;
        float lng = gpsData.isValid ? gpsData.longitude : 0.0;
        
        bool success = gsmHandler.sendAlertTrigger(lat, lng);
        if (success) {
            alertIsActive = true;
            lastLocationUpdate = millis();
            // TODO: Parse actual `alert_id` from the HTTP response
            // For now assuming we just start sending location updates with device_id or temp logic.
        } else {
            // Retry logic could be added here
            Serial.println("Alert trigger failed, will retry on next button hold or implement retry queue.");
            buttonHandler.resetSOS(); // Reset to allow re-trigger
        }
    }

    // 3. Periodic Location Updates if Alert is Active
    if (alertIsActive && (millis() - lastLocationUpdate > LOCATION_UPDATE_RATE_MS)) {
        lastLocationUpdate = millis();
        GPSData gpsData = gpsHandler.getLatestData();
        
        if (gpsData.isValid) {
            Serial.println("Sending periodic location update...");
            gsmHandler.sendLocationUpdate(currentAlertId, gpsData.latitude, gpsData.longitude);
        } else {
            Serial.println("Skipping update, no valid GPS lock.");
        }
    }

    // Small delay to prevent watchdog panic
    delay(10);
}
