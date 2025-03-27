import socket
import threading
import time
import argparse
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Constants
PORT_RANGE_START = 10000
PORT_RANGE_END = 14000
BATCH_SIZE = 100

def get_public_ip():
    """Get the public IP address of this machine."""
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except Exception as e:
        logging.error(f"Failed to get public IP: {e}")
        return input("Could not automatically detect public IP. Please enter your public IP: ")

class P2PChat:
    def __init__(self, my_public_ip, peer_public_ip, is_peer_a=True):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', 5000))
        self.peer_address = None
        self.connected = False
        self.my_public_ip = my_public_ip
        self.peer_public_ip = peer_public_ip
        self.is_peer_a = is_peer_a
        self.stop_flag = False

    def send_heartbeat(self):
        """Send heartbeat messages to maintain the connection."""
        while not self.stop_flag:
            if self.peer_address:
                try:
                    message = f"HEARTBEAT:{self.my_public_ip}"
                    self.socket.sendto(message.encode(), self.peer_address)
                except Exception as e:
                    logging.error(f"Error sending heartbeat: {e}")
            time.sleep(1)

    def listen_for_messages(self):
        """Listen for incoming messages and handle them."""
        while not self.stop_flag:
            try:
                data, addr = self.socket.recvfrom(1024)
                message = data.decode()

                # Verify the sender's IP
                sender_ip = addr[0]
                if sender_ip != self.peer_public_ip:
                    logging.warning(f"Received message from unknown IP: {sender_ip}")
                    continue

                if message.startswith("HEARTBEAT:"):
                    if not self.connected:
                        self.peer_address = addr
                        self.connected = True
                        logging.info(f"Connected to peer at {addr}")
                    self.socket.sendto(f"ACK:{self.my_public_ip}".encode(), addr)
                elif message.startswith("ACK:"):
                    if not self.connected:
                        self.peer_address = addr
                        self.connected = True
                        logging.info(f"Connected to peer at {addr}")
                else:
                    print(f"\nPeer: {message}")

            except Exception as e:
                if not self.stop_flag:
                    logging.error(f"Error receiving message: {e}")

    def send_message(self, message):
        """Send a chat message to the peer."""
        if self.peer_address:
            try:
                self.socket.sendto(message.encode(), self.peer_address)
            except Exception as e:
                logging.error(f"Error sending message: {e}")
        else:
            logging.warning("No peer connection established yet")

    def start(self):
        """Start the chat application."""
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        threading.Thread(target=self.send_heartbeat, daemon=True).start()

        if not self.is_peer_a:
            logging.info("Starting port scanning...")
            self.scan_ports()

        while not self.stop_flag:
            try:
                if self.connected:
                    message = input("You: ")
                    if message.lower() == 'exit':
                        self.stop_flag = True
                        break
                    self.send_message(message)
                else:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.stop_flag = True
                break

    def scan_ports(self):
        """Scan ports to establish connection with Peer A."""
        for port in range(PORT_RANGE_START, PORT_RANGE_END, BATCH_SIZE):
            if self.connected or self.stop_flag:
                break
            
            batch_end = min(port + BATCH_SIZE, PORT_RANGE_END)
            logging.info(f"Scanning ports {port}-{batch_end}")
            
            for test_port in range(port, batch_end):
                try:
                    message = f"HEARTBEAT:{self.my_public_ip}"
                    self.socket.sendto(message.encode(), (self.peer_public_ip, test_port))
                except Exception as e:
                    logging.error(f"Error in port scanning: {e}")
                    break
                
                if self.connected:
                    break
                    
            time.sleep(0.1)

def main():
    # Get public IPs
    my_public_ip = get_public_ip()
    logging.info(f"Your public IP: {my_public_ip}")
    peer_public_ip = input("Enter peer's public IP: ")

    # Determine peer role
    while True:
        role = input("Select role (1 for Peer A - initiator, 2 for Peer B - receiver): ")
        if role in ['1', '2']:
            break
        print("Invalid input. Please enter 1 or 2.")

    is_peer_a = (role == '1')
    role_name = "Peer A (initiator)" if is_peer_a else "Peer B (receiver)"
    logging.info(f"Starting as {role_name}")

    # Create and start chat
    chat = P2PChat(my_public_ip, peer_public_ip, is_peer_a)
    chat.start()

if __name__ == "__main__":
    main()