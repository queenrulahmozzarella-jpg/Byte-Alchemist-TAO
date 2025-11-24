import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, AdamW
from .utils import log
from .config import Config

cfg = Config()

class SimpleCodeDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.examples = [tokenizer(t, truncation=True, max_length=max_length, padding="max_length", return_tensors="pt") for t in texts]

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        item = {k:v.squeeze(0) for k,v in self.examples[idx].items()}
        return item

def train(model_name: str, train_texts, epochs=1, batch_size=2, lr=5e-5):
    log("Starting training loop")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    ds = SimpleCodeDataset(train_texts, tokenizer)
    dl = DataLoader(ds, batch_size=batch_size, shuffle=True)

    opt = AdamW(model.parameters(), lr=lr)
    model.train()
    for epoch in range(epochs):
        for batch in dl:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = input_ids.clone()
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            opt.step()
            opt.zero_grad()
            log(f"Epoch {epoch} loss={loss.item()}")
    # save
    model.save_pretrained("./byte_alchemist_finetuned")
    tokenizer.save_pretrained("./byte_alchemist_finetuned")
    log("Training finished and model saved to ./byte_alchemist_finetuned")
