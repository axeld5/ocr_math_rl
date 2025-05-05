import torch
import json
from PIL import Image
from datasets import Dataset
from transformers import AutoProcessor, AutoModelForImageTextToText, TrainingArguments, Trainer, BitsAndBytesConfig
from dotenv import load_dotenv

load_dotenv()
model_id = "HuggingFaceTB/SmolVLM2-256M-Video-Instruct" 

device = "cuda"
model = AutoModelForImageTextToText.from_pretrained(model_id, device_map="auto", torch_dtype=torch.bfloat16, attn_implementation="eager").to(device) #quantization_config=bnb_config)
processor = AutoProcessor.from_pretrained(model_id)
image_token_id = processor.tokenizer.additional_special_tokens_ids[
            processor.tokenizer.additional_special_tokens.index("<image>")]

def collate_fn(examples):
    texts = []
    images = []
    for example in examples:
        image = Image.open(example["image_path"])
        if image.mode != 'RGB':
            image = image.convert('RGB')
        question = "Answer the question from the image."
        answer = example["model_response"]
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image"},
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": answer}
                ]
            }
        ]
        text = processor.apply_chat_template(messages, add_generation_prompt=False)
        texts.append(text.strip())
        images.append([image])

    batch = processor(text=texts, images=images, return_tensors="pt", padding=True)
    labels = batch["input_ids"].clone()
    labels[labels == processor.tokenizer.pad_token_id] = -100
    labels[labels == image_token_id] = -100
    batch["labels"] = labels

    return batch


#for param in model.vision_tower.parameters():
#    param.requires_grad = False

#for param in model.multi_modal_projector.parameters():
#    param.requires_grad = False

args = TrainingArguments(
    num_train_epochs=10,
    remove_unused_columns=False,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    warmup_steps=2,
    learning_rate=2e-5,
    weight_decay=1e-6,
    adam_beta2=0.999,
    logging_steps=100,
    optim="adamw_hf",
    save_strategy="steps",
    save_steps=1000,
    push_to_hub=True,
    save_total_limit=1,
    output_dir="smolvlm2_ocr_thinking",
    bf16=True,
    report_to=["tensorboard"],
    dataloader_pin_memory=False
)

train_ds = Dataset.from_dict(json.load(open("train_set/train_info.json")))

trainer = Trainer(
    model=model,
    train_dataset=train_ds,
    data_collator=collate_fn,
    args=args
)

trainer.train()