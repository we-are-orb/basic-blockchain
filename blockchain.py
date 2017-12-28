from hashlib import sha256
from time import time
import json


class Blockchain:

    def __init__(self, authors, name="blockchain"):
        """
        Creates a blockchain with genesis block

        :param authors: <list> a list of registered users
        :param name: <str> name of the blockchain,default is 'blockchain'
        :return: <object> blockchain object
        """
        self.name = name
        self.authors = authors
        self.chain = []
        self.current_docs = []
        self.blocksize = 5

        # create genesis block
        genesis = self.create_block(parent_hash=1)
        self.add_block(genesis)

    @staticmethod
    def hash_it(hash_item):
        """
        Creates a hash for a block or doc item

        :param hash_item: <dict> Block item or doc item
        :return: <str> The hash value of hash item
        """
        hash_item = json.dumps(hash_item, sort_keys=True).encode()
        return sha256(hash_item).hexdigest()

    def create_doc(self, author, content):
        """
        Creates a new document

        :param author: <str> Name of author
        :param content: <str> DOcument contents
        :return: <dict> Created block
        """
        doc = {
            "author": author,
            "content": content,
            "timestamp": time(),
        }

        doc_hash = self.hash_it(doc)

        return {"doc_hash": doc_hash, "doc": doc}

    def is_valid_doc(self, doc):
        """
        Checks doc validation

        :param doc: <dict> Document
        """
        if doc["doc"]["author"] in self.authors:
            return True
        else:
            return False

    def add_doc(self, doc):
        if self.is_valid_doc(doc):
            self.current_docs.append(doc)
            print("added to docs pool")
        else:
            print("doc invalid, unregistered author")

    def create_block(self, parent_hash=None):
        """
        Creates a new block

        :param parent_hash: <str> (Optional), used once to create 
                            genesis block
        :return: <dict> Created block
        """
        block = {
            "index": len(self.chain) + 1,
            "parent_block_hash": parent_hash or self.chain[-1]["block_hash"],
            "timestamp": time(),
            "docs": self.current_docs,
        }

        block_hash = self.hash_it(block)

        return {"block_hash": block_hash, "block": block}

    def is_valid_block(self, block):
        """
        Checks if a given block passes the block limit protocol

        :param block: <dict> Block item
        :return: <bool> True for valid and False for invalid
        """
        docs_total = len(self.current_docs)
        if docs_total < self.blocksize:
            return True
        else:
            return False

    def add_block(self, block):
        """
        Adds created block to the blockchain if valid

        :param block: <dict> Block item
        :return: <str> Block item info if valid and warning if not
        """
        if self.is_valid_block(block):
            self.chain.append(block)
            self.current_docs = []
            return "success \n {}".format(block)
        else:
            return "invalid block"

