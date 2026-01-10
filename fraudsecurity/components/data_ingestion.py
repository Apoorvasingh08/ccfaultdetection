import os
import sys
from fraudsecurity.exception import CustomException
from fraudsecurity.logger import logging
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts','train.csv')
    test_data_path: str=os.path.join('artifacts','test.csv')
    raw_data_path: str=os.path.join('artifacts','data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the Data ingestion method")
        try:
            ROOT_DIR = Path(__file__).resolve().parents[2]
            DATA_PATH = ROOT_DIR / "artifacts" / "clean_raw_data.csv"

            df = pd.read_csv(DATA_PATH)
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path , index=False,header=True)

            logging.info("train test split initiated.")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path , index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("ingestion of data is completed.")
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ =="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

