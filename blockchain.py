import hashlib
import time

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        new_block = Block(len(self.chain), data, self.get_last_block().hash)
        self.proof_of_work(new_block)
        self.chain.append(new_block)
        print(f"Block {new_block.index} mined: {new_block.hash}")

    def proof_of_work(self, block):
        while not block.hash.startswith("0" * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            if current.hash != current.calculate_hash():
                print(f"Block {i} has invalid hash")
                return False

            if current.previous_hash != previous.hash:
                print(f"Block {i} has invalid previous hash")
                return False

            if not current.hash.startswith("0" * self.difficulty):
                print(f"Block {i} does not meet difficulty")
                return False
        return True

my_chain = Blockchain()


my_chain.add_block("Block 1 Data")
my_chain.add_block("Block 2 Data")
my_chain.add_block("Block 3 Data")

print("\nIs blockchain valid?", my_chain.is_chain_valid())


my_chain.chain[1].data = "Tampered Data"
print("\nAfter tampering, is blockchain valid?", my_chain.is_chain_valid())


