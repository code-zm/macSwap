import os
import subprocess
import secrets
import time
import customtkinter as ctk
from tkinter import messagebox
import re  

# set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# create the main application window
app = ctk.CTk()
app.title("code-zm")
app.geometry("400x500")  # set  window size

app.grid_columnconfigure(0, weight=1)  # left padding
app.grid_columnconfigure(1, weight=0)  # main content
app.grid_columnconfigure(2, weight=1)  # right padding for balance

# function to get sudo permissions at startup
def requestSudo():
    try:
        subprocess.run(["sudo", "-v"], check=True)
    except subprocess.CalledProcessError:
        messagebox.showerror("Permission Denied", "Sudo permissions are required to change the MAC address.")
        app.quit()

# add a title label at the top center
titleLabel = ctk.CTkLabel(app, text="macSwap", font=("Helvetica", 20, "bold"))
titleLabel.grid(row=0, column=1, pady=20)

# function to get a list of  network interfaces using `ip a`
def getNetworkInterfaces():
    try:
        result = subprocess.run(["ip", "a"], capture_output=True, text=True, check=True)
        output = result.stdout
        interfaces = {}
        for line in output.splitlines():
            if "state UP" in line or "state DOWN" in line:
                parts = line.split()
                interfaceName = parts[1].strip(":")
                if interfaceName.startswith("e"):
                    interfaces[f"{interfaceName} (Ethernet)"] = interfaceName
                elif interfaceName.startswith("w"):
                    interfaces[f"{interfaceName} (Wi-Fi)"] = interfaceName
        return interfaces
    except subprocess.CalledProcessError as e:
        print("Error fetching interfaces:", e)
        messagebox.showerror("Error", f"Failed to get active network interfaces: {e}")
        return {}

def getCurrentMac(interface):
    try:
        result = subprocess.run(["ip", "link", "show", interface], capture_output=True, text=True, check=True)
        output = result.stdout
        for line in output.splitlines():
            if "link/ether" in line:
                macAddress = line.split()[1]
                return macAddress
        print(f"No MAC address found for {interface}.")
        return "Unknown MAC"
    except subprocess.CalledProcessError as e:
        print("Error fetching MAC address:", e)
        messagebox.showerror("Error", f"Failed to get MAC address: {e}")
        return "Error"

# function to update the current mac address display
def updateMacDisplay(*args):
    selectedInterface = interfaceOptionMenu.get()
    if selectedInterface in networkInterfaces:
        actualInterface = networkInterfaces[selectedInterface]
        currentMac = getCurrentMac(actualInterface)
        currentMacLabel.configure(text=f"Current MAC Address: {currentMac}")

# function to generate a random mac address
def generateRandomMac():
    mac = [secrets.randbelow(256) for _ in range(6)]
    # set MAC to be globally unique & unicast
    mac[0] = mac[0] & 0xfc
    randomMacStr = ':'.join(f"{x:02x}" for x in mac)

    macEntry.delete(0, ctk.END)
    macEntry.insert(0, randomMacStr)

# function to validate input and then change mac address
def changeMac():
    macAddressRegex = r'^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$'
    
    userFriendlyInterface = interfaceOptionMenu.get()
    interface = networkInterfaces.get(userFriendlyInterface)
    newMac = macEntry.get()
    
    if not interface or not newMac:
        print("Interface or MAC address not provided.")
        messagebox.showerror("Input Error", "Please provide both the interface and the new MAC address.")
        return

    if not re.match(macAddressRegex, newMac):
        print("Invalid MAC address format.")
        messagebox.showerror("Invalid MAC", "The MAC address format is incorrect. Please enter a valid MAC address (XX:XX:XX:XX:XX:XX).")
        return

    try:
        print(f"Bringing down {interface}.")
        time.sleep(0.5)
        subprocess.run(["sudo", "ip", "link", "set", interface, "down"], check=True)
        print(f"Changing MAC to {newMac}")
        time.sleep(0.5)
        subprocess.run(["sudo", "ip", "link", "set", interface, "address", newMac], check=True)
        subprocess.run(["sudo", "ip", "link", "set", interface, "up"], check=True)
        print(f"Activating {interface}.")
        messagebox.showinfo("Success", f"MAC address changed to {newMac} on {interface}.")
        updateMacDisplay()
    except subprocess.CalledProcessError as e:
        print("Error changing MAC address:", e)
        messagebox.showerror("Error", f"Failed to change MAC address: {e}")

def resetFields():
    macEntry.delete(0, ctk.END)

# request sudo permissions at startup
requestSudo()

# get network interfaces
networkInterfaces = getNetworkInterfaces()

# interface selection ui elements
interfaceLabel = ctk.CTkLabel(app, text="Select Network Interface:")
interfaceLabel.grid(row=1, column=1, pady=5)

interfaceOptionMenu = ctk.CTkOptionMenu(app, values=list(networkInterfaces.keys()), command=updateMacDisplay, width=200)
interfaceOptionMenu.grid(row=2, column=1, pady=5)
if networkInterfaces:
    interfaceOptionMenu.set(list(networkInterfaces.keys())[0])

# define the current mac label so it can be referenced in updateMacDisplay
currentMacLabel = ctk.CTkLabel(app, text="Current MAC Address:")
currentMacLabel.grid(row=3, column=1, pady=10)

# display current MAC on startup after defining currentMacLabel
updateMacDisplay()

# mac address input
macLabel = ctk.CTkLabel(app, text="New MAC Address:")
macLabel.grid(row=4, column=1, pady=5)

macEntry = ctk.CTkEntry(app, width=300)
macEntry.grid(row=5, column=1, pady=5)

# generate random mac button
generateMacButton = ctk.CTkButton(app, text="Generate Random MAC", command=generateRandomMac, width=200)
generateMacButton.grid(row=6, column=1, pady=10)

# change mac button
changeButton = ctk.CTkButton(app, text="Change MAC Address", command=changeMac, width=200)
changeButton.grid(row=7, column=1, pady=10)

# reset fields button
resetButton = ctk.CTkButton(app, text="Reset", command=resetFields, width=200)
resetButton.grid(row=8, column=1, pady=10)

app.mainloop()
