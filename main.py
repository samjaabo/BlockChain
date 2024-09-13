"""
Disclaimer:

Please note that I am only learning about Web3
and blockchain technology, and my involvement is purely for educational purposes.
I do not engage in any illegal activities.
and I fully comply with the laws and regulations of Morocco.
"""


import hashlib
import time

class Block:

    def __init__(self, index,  data, prev_hash=None):
        self.index = index
        self.prev_hash = prev_hash
        self.timestamp = time.time()
        self.data = data
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def get_merged_block(self):
        return f"{self.index}\n{self.prev_hash}\n{self.timestamp}\n{self.data}\n{self.nonce}"
    
    def calculate_hash(self):
        block_data = self.get_merged_block()
        return hashlib.sha256(block_data.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        # print("Start mining the block ...")
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        # print("Block has been mined")
        # print(self.get_merged_block())
        # print(self.hash)
    
    def __str__(self):
        return f"{self.index}:{self.hash}"

    def __repr__(self):
        return self.__str__()


class BlockChainDifficulty:
    """
    Automatic adjust difficulty to meet the specified time.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.difficulty = 4
        self.blocks_mine_time = [] # minig time of blocks
        self.target_seconds_time = 5 # target time to mine a block
        self.adjust_mine_time_interval = 3 # how many block can be mined before adjusting the difficulty

    def adjust_difficulty(self, first_time=False):
        total_time = sum(self.blocks_mine_time)
        average_time_per_block = total_time / self.adjust_mine_time_interval
        # print("average: ", average_time_per_block)
        if average_time_per_block < self.target_seconds_time:
            if self.difficulty < 4:
                # this is for test only
                self.difficulty += 1
        elif average_time_per_block > self.target_seconds_time:
            self.difficulty = max(1, self.difficulty - 1)
        # print("difficulty is adjusted to: ", self.difficulty)
        self.blocks_mine_time = []


class BlockChain(BlockChainDifficulty):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chain = [self.create_genesis_block()]
        
    def create_genesis_block(self):
        return Block(0,  "Genesis block", prev_hash="0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, new_block):
        new_block.prev_hash = self.get_latest_block().hash
        start_time = time.time()
        new_block.mine_block(self.difficulty)
        end_time = time.time()
        self.chain.append(new_block)

        full_time = end_time - start_time
        self.blocks_mine_time.append(full_time)

        if len(self.chain) % self.adjust_mine_time_interval == 0:
            # print("--->" ,len(self.chain))
            self.adjust_difficulty()
    
    def print(self):
        for block in self.chain:
            print(block)


blockchain = BlockChain()

start_time = time.time()
for i in range(1, 24):
    block = Block(i, f"Hello, World! {i}")
    blockchain.add_block(block)
end_time = time.time()
full_time = end_time - start_time
print("The time took for 10 blocks to be mined is: ", full_time, "Seconds")
blockchain.print()
# blockchain.chain[3].hash = "0xfffffff"
# blockchain.print()