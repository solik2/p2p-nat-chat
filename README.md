# P2P NAT Chat

A peer-to-peer chat application that uses brute force port scanning for NAT traversal, enabling direct communication between peers even when behind NAT.

## Features

- Direct P2P communication
- NAT traversal using brute force port scanning
- Automatic public IP detection
- Simple command-line interface
- Works across different networks

## Requirements

- Python 3.9 or higher
- Conda (recommended) or pip

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/solik2/p2p-nat-chat.git
   cd p2p-nat-chat
   ```

2. Create and activate a conda environment:
   ```bash
   conda create -n p2p-chat python=3.9
   conda activate p2p-chat
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the program on both computers:

```bash
python p2p_chat.py
```

The program will:
1. Automatically detect your public IP
2. Ask for the other peer's public IP
3. Ask you to select a role:
   - Option 1: Peer A (initiator)
   - Option 2: Peer B (receiver)

### Important Notes

- Both peers must be on different networks (different public IPs)
- Port 5000 must be available on both computers
- Peer A must start first
- The program verifies IP addresses to ensure message authenticity

## How It Works

1. Initial Setup:
   - Peer A (initiator) listens on port 5000
   - Peer B (receiver) also listens on port 5000

2. Connection Establishment:
   - Peer B performs brute force scanning to find Peer A
   - Once connected, both peers can send messages

3. NAT Traversal:
   - Uses UDP hole punching technique
   - Maintains connection with heartbeat messages

## Troubleshooting

- If connection fails:
  - Ensure both peers are using correct public IPs
  - Check if port 5000 is available
  - Verify firewall settings

- If public IP detection fails:
  - The program will prompt you to enter it manually
  - You can find your public IP at https://api.ipify.org

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.