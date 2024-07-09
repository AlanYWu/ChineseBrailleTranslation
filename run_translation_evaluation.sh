#!/bin/bash
set -e

output_dir="./output-dirs/evaluation-final"
accelerate launch --main_process_port 31111 run_translation.py \
    --model_name_or_path "Violet-yo/mt5-small-ft-Chinese-Braille" \
    --output_dir $output_dir \
    --dataset_name "Violet-yo/Chinese-Braille-Dataset-10per-Tone" \
    --do_eval \
    --do_predict \
    --per_device_eval_batch_size=48 \
    --fp16 False \
    --predict_with_generate \
    --overwrite_output_dir True \
    --eval_strategy "steps" \
    --logging_dir "$output_dir/running_logs/" \
    --seed 42 \
    --eval_steps 10000 \
    --logging_steps 1 \
    --max_source_length 285 \
    --max_target_length 285 \
    --val_max_target_length 300 \
    --generation_max_length 300 \
    --generation_num_beams 5 \
    --use_fast_tokenizer False \
    --preprocessing_num_workers 8 \
    --lr_scheduler_type cosine \
    --learning_rate 1e-5
