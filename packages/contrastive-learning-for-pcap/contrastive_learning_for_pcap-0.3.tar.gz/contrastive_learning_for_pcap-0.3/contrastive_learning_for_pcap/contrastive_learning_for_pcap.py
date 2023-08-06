from traceback import extract_tb
import pandas as pd 
import numpy as np
from torch.utils.data import DataLoader
from os import walk
from sentence_transformers import SentenceTransformer, InputExample
from sentence_transformers import models, losses
from tqdm import tqdm
from scapy.all import *

class contrastive_learning_for_pcap():
    def __init__(self, path, target=None):
        self.path = path
        self.target = target
        self.file_names = next(walk(path), (None, None, []))[2]
        self.word_embedding_model = models.Transformer('distilroberta-base', max_seq_length=32)
        self.pooling_model = models.Pooling(self.word_embedding_model.get_word_embedding_dimension())
        self.embedding_model = SentenceTransformer(modules=[self.word_embedding_model, self.pooling_model])
        self.data=None

    # Extract substring of bytes
    def __clean_string_for_bytes(self,s):
        end = s.find(".")
        substring = s[:end]
        return substring

    # Received PCAP file and return list with the bytes strings
    def __extract_hexadecimal_from_pcap(self, file_name):
        samples=[]
        pcap_file = rdpcap(self.path + '/'+file_name )
        plist = PacketList([p for p in pcap_file])
        for i in tqdm( range(len(plist)) ):
            s= scapy.utils.linehexdump(plist[i], dump=True)
            s=self.__clean_string_for_bytes(s)
            samples.append(s)
        return pd.DataFrame(samples)

    def __extract_hex(self):
        hex_df = pd.DataFrame()
        for file_name in self.file_names:
            pcap_df= self.__extract_hexadecimal_from_pcap(file_name)
            #pcap_df['target'] = self.target
            #pcap_df['group'] = file_name
            hex_df= hex_df.append(pcap_df, ignore_index=True)
        return hex_df

    def fit(self, epochs_num=1):

        # Preprocessing for extracting the bytes representation
        data_df= self.__extract_hex()
        self.data= data_df.iloc[:, 0]
        # Convert train sentences to sentence pairs
        train_data = [InputExample(texts=[s, s]) for s in self.data]

        # DataLoader to batch your data
        train_dataloader = DataLoader(train_data, batch_size=128, shuffle=True)

        # Use the denoising auto-encoder loss
        train_loss = losses.MultipleNegativesRankingLoss(self.embedding_model)

        # Fit method
        self.embedding_model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=epochs_num)


    def transform(self, path):

        # Transform the data
        data_encoded = self.embedding_model.encode(self.data)
        return data_encoded


    def fit_transform(self, epochs_num=1):

        # Preprocessing for extracting the bytes representation
        data_df= self.__extract_hex()
        self.data= data_df.iloc[:, 0]

        # Convert train sentences to sentence pairs
        train_data = [InputExample(texts=[s, s]) for s in self.data]

        # DataLoader to batch your data
        train_dataloader = DataLoader(train_data, batch_size=128, shuffle=True)

        # Use the denoising auto-encoder loss
        train_loss = losses.MultipleNegativesRankingLoss(self.embedding_model)

        # Fit method
        self.embedding_model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=epochs_num)
        data_encoded = self.embedding_model.encode(self.data)

        return data_encoded