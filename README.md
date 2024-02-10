# theScore

## Tested on the Following Setup:

### APP:
  - v24.2.0 (Android 7.0+)
  - [theScore: Sports News & Scores v24.2.0](https://www.apkmirror.com/apk/thescore-inc/thescore-live-sports-scores-news-stats-videos/thescore-live-sports-scores-news-stats-videos-24-2-0-release/)

### Appium:
  - Appium v2.0.1
  - Make sure uiautomator2 is installed (for android)
      - Can be installed with: 
        - `appium driver install uiautomator2`

### Java:
  - Using Java version "20.0.1" 2023-04-18
    - **Note:** _UiAutomator2 is compatible with Java11_

### Android Studio
  - Android Studio Hedgehog | 2023.1.1 Patch 2
  - Build #AI-231.9392.1.2311.11330709, built on January 18, 2024
  - Runtime version: 17.0.7+0-17.0.7b1000.6-10550314 aarch64
  - VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.

### System:
  - **OS**: macOS 14.2.1
  - **Chip**: Apple M2 Pro

### Phone:
- virtual on Android Studio
  - model: Pixel 7 Pro API 34
  - OS: Android 14.0]

### Python:
- [Python 3.9.X](https://www.python.org/downloads/release/python-3918/)

## Setup
### Requirements:
- Install python requirements with the following:
  - `pip install -r requirments.txt`
### Appium:
- Have **_ANDROID_SDK_ROOT_** or **_ANDROID_HOME_** environment variable set to **SDK** path.
- Start appium:
  - `appium -p <port> --base-path /wd/hub`
    - where port is **_4743_**, that can be changed to a different port.


