#!/bin/bash
set -e

output_dir="./output-dirs/finetune-mt5"
accelerate launch run_translation.py \
    --model_name_or_path models/mt5-braille \
    --output_dir $output_dir \
    --dataset_name "Violet-yo/Chinese-Braille-Dataset-Full-Tone" \
    --do_train \
    --do_eval \
    --num_train_epochs 5.0 \
    --per_device_train_batch_size=24 \
    --per_device_eval_batch_size=24 \
    --fp16 False \
    --predict_with_generate \
    --overwrite_output_dir True \
    --eval_strategy "steps" \
    --logging_dir "$output_dir/running_logs/" \
    --seed 42 \
    --eval_steps 1000 \
    --logging_steps 1 \
    --max_source_length 285 \
    --max_target_length 285 \
    --val_max_target_length 300 \
    --use_fast_tokenizer False \
    --preprocessing_num_workers 8
