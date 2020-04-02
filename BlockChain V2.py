#!/usr/bin/env python
# coding: utf-8

# In[418]:


# import libraries
import hashlib
import random
import string
import json
import binascii
import datetime
import collections


# In[419]:


import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5



# In[420]:




# Client Class generate the public and private keys
class Client:
    def __init__(self):
        random=Crypto.Random.new().read
        self._private_key=RSA.generate(1024,random)
        self._public_key=self._private_key.publickey()
        self._signer=PKCS1_v1_5.new(self._private_key)
        
# The generated public key will used as the client's identity  
# it returns HEX representation of the public key

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
   


# In[436]:


# Creates an instance of Client and assigns it to the variable Kavindu. 
# We print the public key of Kavindu by calling its identity property
Kavindu = Client()
print (Kavindu.identity)


# In[422]:


#in Transaction class, client will be able to send money to somebody.
transactions = []
last_block_hash=""

class Transaction:

    def __init__(self, sender,recipient, value):
        # senders public key
        self.sender=sender
        
        #Recivers public key
        self.recipient=recipient
        
        # Amount to be sent
        self.value=value
        
        # Time of Transaction
        self.time=datetime.datetime.now()
        
 # Combine all 4 variables to a dictionary object       
    def to_dict(self):
        if self.sender=="Genesis":
            identity="Genesis"
            
        else:
            identity=self.sender.identity
            
       # Construct the dictionary     
        return collections.OrderedDict({'sender': identity,'recipient': self.recipient,'value': self.value,'time' : self.time})
        
      # We sign the dictionary object using the private key of the sender  
    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        
        return binascii.hexlify(signer.sign(h)).decode('ascii')
    
    
def display_transaction(transaction):
         #for transaction in transactions:
        dict = transaction.to_dict()
        print ("sender: " + dict['sender'])
        print ('-----')
        print ("recipient: " + dict['recipient'])
        print ('-----')
        print ("value: " + str(dict['value']))
        print ('-----')
        print ("time: " + str(dict['time']))
        print ('-----')
        
    
    


# In[423]:


# Test Transaction class
Lakshan = Client()
indunil = Client()

# Lakshan send 5 TPC coins to  indunil
t = Transaction(Lakshan,indunil.identity,5.0)

signature = t.sign_transaction()
print (signature)


# In[437]:



Kavinda = Client()
lakshan = Client()
Indunil = Client()
Dushan = Client()

t1 = Transaction(Kavinda,Indunil.identity,15.0)
t1.sign_transaction()
transactions.append(t1)

t2 = Transaction(Indunil,Dushan.identity,6.0)
t2.sign_transaction()
transactions.append(t2)

t3 = Transaction(lakshan,Indunil.identity,2.0)
t3.sign_transaction()
transactions.append(t3)

t4 = Transaction(lakshan,Dushan.identity,4.0)
t4.sign_transaction()
transactions.append(t4)

t5 = Transaction(Kavinda,Dushan.identity,7.0)
t5.sign_transaction()
transactions.append(t5)


# In[438]:



for transaction in transactions:
    display_transaction(transaction)
    print ('--------------')


# In[426]:


class Block:
    
    def __init__(self):
        self.verified_transaction=[]
        self.previous_block_hash=""
        self.Nonce=""


# In[427]:


# Create a Client object 
Mahee=Client()

# Create a transaction Object 
t0 = Transaction ("Genesis",Mahee.identity,500.0)

# Create a block Object
# Here we create a Genises Block 
block0=Block()
block0.verified_transaction.append(t0)
block0.previous_block_hash=None
Nonce=None

# Hash the entire block 
digest=hash(block0)

# Assign the hashed value to variable last_block_hash
last_block_hash=digest


# In[428]:


# TPCoins store the Blocks
TPCoins=[]

def dump_blockchain (self):
    print ("Number of blocks in the chain: " + str(len (self)))
    
    for x in range (len(TPCoins)): # loop through the TPCoins array
        
        # assign each block in TPCoins to a temp variable block_temp
        block_temp = TPCoins[x]  
        print ("block # " + str(x))
        
        # display the transactions inside the block
        for transaction in block_temp.verified_transaction:
            display_transaction (transaction)
            print ('--------------')
            
        print ('=====================================')              


# In[429]:


# Append the Genesis block to TPCoins 
TPCoins.append(block0)
dump_blockchain(TPCoins)


# In[430]:


#Mining process
#The sha256 function takes a message as a parameter, encodes it to ASCII, generates a hexadecimal digest and returns 
#the value to the caller.

def sha256(message):
    return hashlib.sha256(message.encode('ascii')).hexdigest()


# In[431]:


# Develop a Mine function
# Here it tries to find the solution to that one NOnce that will satisfy the hash for the block
# We send the block and the difficulty level as the parameters to the mine function.

def mine(message,difficulty=1):
    #The difficulty level needs to be greater or equal to 1, we ensure this with the following assert statement:
    assert difficulty >= 1  
    
    #We create a prefix variable using the set difficulty level.
    prefix = '1' * difficulty  
    
    for i in range(1000):
        digest = sha256(str(hash(message)) + str(i)) 
        
        if digest.startswith(prefix):
            print ("after " + str(i) + " iterations found nonce: "+ digest)
            return digest
    


# In[432]:


# Test the mine function
mine("test message", 2)


# In[433]:


#Miner 2 adds a block
last_transaction_index=0
block = Block()

# append 3 transactions to block
for i in range(3):
    temp_transaction = transactions[last_transaction_index]
    # validate transaction
    # if valid
    block.verified_transaction.append (temp_transaction)
    last_transaction_index += 1
    
# Assign the value of last_block_hash to the previous_block_hash attribute in the block    
block.previous_block_hash = last_block_hash

# Send the block which has (Transactions + previous_bloc_hash) for the mine function 
block.Nonce = mine (block, 2)

TPCoins.append (block)

# Hased the currrent block and store its hashed value in the last_block_hash variable 
digest = hash (block)
#print("Block hash of the current Block "+ str(digest))
last_block_hash = digest


# In[434]:


dump_blockchain(TPCoins)


# In[ ]:




