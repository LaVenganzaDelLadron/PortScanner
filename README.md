# ADB Port Scanner

This Python script scans a target IP address or subnet for open ADB (Android Debug Bridge) ports and attempts to connect to them using the `adb connect` command. It helps identify devices with accessible ADB interfaces over the network.

---

## Features

- Scans ports in the range 0 to 99999 (adjustable in the script).
- Supports scanning a single IP or an IP range/subnet (e.g., `192.168.1.0/24`).
- Concurrent scanning using threads for faster results.
- Attempts to establish ADB connections to open ports.
- Displays connection success or failure messages with timestamps.

---

## Requirements

- Python 3.x
- `adb` (Android Debug Bridge) installed and accessible in your system's PATH.
- Network access to the target IP(s).

---

## Usage

1. Clone or download this repository.

2. Ensure `adb` is installed on your system. You can check by running:

    ```bash
    adb version
    ```

3. Run the script:

    ```bash
    python3 portscanner.py
    ```

4. When prompted, enter a target IP address or range:

    - Single IP example: `192.168.1.5`
    - IP range example: `192.168.1.0/24`

5. The script will scan ports and attempt ADB connections, printing the results live.

---

## Example Output

