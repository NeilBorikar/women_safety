#ifndef CONFIG_H
#define CONFIG_H

#ifdef __cplusplus
extern "C" {
#endif

// ==========================================
// BACKEND CONFIGURATION
// ==========================================
#define BACKEND_BASE_URL "https://your-api-url.com"  // E.g., Render or local IP via Ngrok
#define API_TRIGGER_ENDPOINT "/alert/trigger"
#define API_LOCATION_ENDPOINT "/location/update"

// Authentication configuration for JWT (set this before flashing!)
#define APP_AUTH_TOKEN "YOUR_JWT_TOKEN_HERE"
#define APP_USER_ID "YOUR_USER_ID_HERE"
#define APP_DEVICE_ID "ESP32_NEO_A7670C"

// ==========================================
// GSM (A7670C) CONFIGURATION
// ==========================================
#define GSM_APN "internet"  // Update with your SIM card's APN

// Hardware Serial 1 pins (GSM)
#define GSM_RX_PIN 16
#define GSM_TX_PIN 17
#define GSM_BAUDRATE 115200

// ==========================================
// GPS (NEO M8L) CONFIGURATION
// ==========================================
// Hardware Serial 2 pins (GPS)
#define GPS_RX_PIN 18
#define GPS_TX_PIN 19
#define GPS_BAUDRATE 9600

// ==========================================
// HARDWARE PINS
// ==========================================
#define SOS_BUTTON_PIN 12      // Push button connected to GPIO12 (pull-down or pull-up expected)
#define BATTERY_ADC_PIN 34     // TP4056 / battery voltage via voltage divider

// ==========================================
// TIMINGS
// ==========================================
#define SOS_DEBOUNCE_DELAY_MS 50   // 50ms standard debounce
#define SOS_HOLD_TIME_MS 2000      // 2 seconds hold to trigger SOS
#define LOCATION_UPDATE_RATE_MS 10000 // Send location every 10 seconds when active

#ifdef __cplusplus
}
#endif

#endif // CONFIG_H
