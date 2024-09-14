
from typing import List, Dict
import openai
from datasets import load_dataset
from tqdm import tqdm

from huggingface_hub import login, list_datasets



mmlu = load_dataset("cais/mmlu", "all")
