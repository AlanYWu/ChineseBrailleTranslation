import evaluate
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

braille_text = "⠼⠓⠙⠁⠃⠉⠊ ⠓⠶⠞⠼ ⠚⠴⠺ ⠤ ⠘ ⠌⠢ ⠛⠊ ⠝⠩ ⠳⠬ ⠊⠓⠑ ⠛⠕⠛⠫ ⠵⠪ ⠵⠼⠛⠫ ⠟⠥⠅⠷⠐ ⠊⠛⠡ ⠃⠔ ⠌⠲⠛⠕ ⠛⠩⠱⠖ ⠙⠢ ⠟⠥⠅⠷⠇⠭ ⠃⠥⠟⠲ ⠱⠦⠇⠪⠐ ⠙⠧⠱ ⠃⠡ ⠍⠮⠳ ⠙⠖ ⠛⠕⠱⠼ ⠙⠢ ⠟⠼⠙⠥ ⠐⠆"
ground_truth = "841239\t黄腾 认为 ： “ 这 几 年 由于 一些 国家 在 增加 出口 ， 已经 把 中国 减少 的 出口量 补充 上来 ， 但是 并 没有 到 过剩 的 程度 。\n"
model = AutoModelForSeq2SeqLM.from_pretrained("Violet-yo/mt5-small-ft-Chinese-Braille")
tokenizer = AutoTokenizer.from_pretrained("Violet-yo/mt5-small-ft-Chinese-Braille", use_fast=False)

inputs = tokenizer(
    braille_text, return_tensors="pt", max_length=280, padding=True, truncation=True
)
output_sequences = model.generate(
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    max_new_tokens=300,
    num_beams=5,
)
translated_text = tokenizer.decode(output_sequences[0], skip_special_tokens=True)
print(f"{translated_text=}")
print(f"{ground_truth=}")
metric = evaluate.load("models/metrics/sacrebleu")
results = metric.compute(predictions=[translated_text], references=[[ground_truth]])
print(f"{results=}")
