# Python Blockchain Implementation

A simple blockchain implementation in Python using Flask as the web framework. 
This project demonstrates the core concepts of blockchain technology including proof-of-work, transaction recording, and decentralized consensus.

## Features

- **Blockchain Core**
  - Genesis block creation
  - Proof-of-work algorithm (with adjustable difficulty)
  - Block creation and chaining
  - Hashing with SHA-256

- **Transaction System**
  - New transaction creation
  - Transaction recording in blocks
  - Mining rewards

- **Network Features**
  - Node registration
  - Consensus algorithm (longest chain rule)
  - Conflict resolution

- **API Endpoints**
  - Mine new blocks
  - Create transactions
  - View blockchain
  - Register nodes
  - Resolve chain conflicts

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/python-blockchain.git
   cd python-blockchain
   ```

2. Install the required dependencies:
   ```
   pip install flask requests uuid
   ```

3. Runt the blockchain node:
   ```
   python blockchain.py
   ```

## API Documentation
### Mine a new block
- Endpoint: ```GET /mine```
- Description: Mines a new block and awards the miner (node) with 1 coin
- Response: Returns the newly mined block details

### Create a new transaction
- Endpoint: POST ```/transactions/new```
- Body:
```json
{
  "sender": "sender_address",
  "recipient": "recipient_address",
  "amount": 1
}
```
- Description: Creates a new transaction to be added to the next mined block
- Response: Returns the block index the transaction will be included in

### Get full blockchain 
- Endpoint: GET ```/chain```
- Description: Returns the full blockchain and its length
- Response:
```
{
  "chain": [...],
  "length": n
}
```

### Register new nodes
- Endpoint: POST ```/nodes/register```
- Body:
```json
{
  "nodes": ["http://node1:5000", "http://node2:5000"]
}
```
- Description: Registers new nodes with the network
- Response: Returns list of all registered nodes

###Consensus
- Endpoint: ```GET /nodes/resolve```
- Description: Resolves blockchain conflicts by choosing the longest valid chain
- Response: Returns the current chain (either replaced or authoritative)

## Dependencies
- Python 3.x
- Flask
- Requests
- UUID
