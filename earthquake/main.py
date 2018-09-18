from earthquake.controllers.gamepad import GamepadEarthquakeController, GamepadController
from earthquake.usb.detector import USBDetector

if __name__ == '__main__':
    USBDetector(GamepadEarthquakeController(GamepadController()))()
