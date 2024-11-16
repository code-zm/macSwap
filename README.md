# macSwap
macSwap is a Python-based GUI tool for MAC address spoofing. Allows users to view their network interfaces and change the MAC addresses for each.  All generated MAC addresses comply with GUA guidelines, providing reliable and standard-compliant spoofing for privacy / testing purposes. 

## Features
- Display all network interfaces.
- View the current MAC address of selected interfaces.
- Generate a random MAC address or manually enter a new MAC address.

## Prerequisites
- Python 3.x
- Running on Linux based OS

## Installation
1. Clone this repository:
```
git clone https://github.com/yourusername/macSwap.git 
cd macSwap
```

2. Set up a virtual environment (recommended):
```
python3 -m venv venv 
source venv/bin/activate  
```

3. Install the dependencies:
```
pip install -r requirements.txt
```

## Usage
1. Run the Application:
```
python macswap.py
```

2. Using the GUI:
- Choose an interface to modify from the dropdown list.
- Click on "Generate Random MAC" to generate a random MAC address or manually enter a MAC address in the provided field.
- Randomize as many times as you like, when you are satisfied, click "Change MAC Address". This will apply the new MAC address to the selected interface.
- The "Reset" button clears the MAC address entry field.

## Notes
- Changing MAC addresses requires `sudo` priveleges
- This program sets the network interface to `DOWN` before changing the MAC address, this will disconnect it from any networks. 
- This only changes your operational MAC address. To restore back to your original, simply reboot. 
