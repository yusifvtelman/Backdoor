# Python Backdoor (Educational Purpose Only)

A simple client-server backdoor implementation in Python for educational purposes. This project demonstrates basic socket programming, remote command execution, and file transfer capabilities.

⚠️ **Disclaimer:** This project is strictly for educational purposes only. Using this code without explicit permission on systems you don't own is illegal and unethical.

## Features

- Remote command execution
- Persistent connection with automatic reconnection
- File upload and download capabilities
- Cross-platform compatibility
- Simple command-line interface

## Requirements

- Python 3.x
- No additional packages required (uses standard library only)

## Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/python-backdoor
cd python-backdoor
```

## Usage

1. Start the server:
```bash
python3 server.py
```

2. Start the client on the target machine:
```bash
python3 client.py
```

### Available Commands

- Execute system commands directly through the shell
- `download <filepath>` - Download a file from the client
- `upload <filepath>` - Upload a file to the client
- `exit` - Close the connection

### Default Configuration

- Default server IP: `127.0.0.1`
- Default port: `4444`

To modify these settings, edit the following variables:
- Server: Edit `host` and `port` in `BackdoorServer` class initialization
- Client: Edit `SERVER_URL` and `PORT` constants at the top of client.py

## Security Considerations

- The connection is currently unencrypted
- No authentication mechanism is implemented
- No input validation is performed
- The backdoor runs with the privileges of the executing user

## Project Structure

```
python-backdoor/
├── README.md
├── server.py    # Server-side implementation
└── client.py    # Client-side implementation
```

## Technical Details

- Uses TCP sockets for reliable communication
- Implements custom protocol for file transfers
- Handles large file transfers with buffering
- Automatic reconnection on connection loss
- Error handling for command execution

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This code is provided for educational purposes only. The author takes no responsibility for any misuse of this code. Always obtain explicit permission before running this code on any system.

