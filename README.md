# ChineseBrailleTranslation
<p align="center">
  📃 <a href="https://arxiv.org/abs/2407.06048/" target="_blank">[Paper]</a> • 💻 <a href="https://github.com/AlanYWu/ChineseBrailleTranslation" target="_blank">[Github]</a> • 🤗 <a href="https://huggingface.co/datasets/Violet-yo/Chinese-Braille-Dataset-10per-Tone" target="_blank">[Dataset]</a> • ⚙️ <a href="https://huggingface.co/Violet-yo/mt5-small-ft-Chinese-Braille" target="_blank">[Model]</a> • 🎬 <a href="https://vision-braille.com/" target="_blank">[Demo]</a>
</p>

## Setup Environment
We recommend using a conda environment to manage dependencies.
```bash
conda create -n chinese_braille python=3.10
conda activate chinese_braille
pip install -r requirements.txt
```
The installation of `pytorch` may vary depending on your system. Please refer to the [official website](https://pytorch.org/get-started/locally/) for more information.

All the training and evaluation scripts use `accelerate` to speed up the training process. If you want to run the scripts without `accelerate`, you can remove the `accelerate` related code in the scripts. Remember to run `accelerate config` before you run our scripts, or you may encounter some errors.

## Data Preparation
Please follow the instructions in the [data_preparation](data_preparation/README.md) folder to prepare the dataset. We also provide three preprocessed dataset in HuggingFace:
- [Violet-yo/Chinese-Braille-Dataset-10per-Tone](https://huggingface.co/datasets/Violet-yo/Chinese-Braille-Dataset-10per-Tone)
- [Violet-yo/Chinese-Braille-Dataset-No-Tone](https://huggingface.co/datasets/Violet-yo/Chinese-Braille-Dataset-No-Tone)
- [Violet-yo/Chinese-Braille-Dataset-Full-Tone](https://huggingface.co/datasets/Violet-yo/Chinese-Braille-Dataset-Full-Tone)

All these three dataset are used in our training.

## Training
### Add Special Tokens
First we need to add the braille characters to the tokenizer. We provide a script to add the special tokens to the tokenizer. You can run the script by:
```bash
python mt5_add_special_tokens.py --original_model_dir $T5_ORIGINAL_DIR --output_dir $T5_SPECIAL_DIR
```
where `$T5_ORIGINAL_DIR` is the directory of the original T5 model and `$T5_SPECIAL_DIR` is the directory to save the new model with special tokens and extended word embedding weights.

### Fine Tuning
We provide an example script in [run_translation_accelerate.sh](./run_translation_accelerate.sh) to train the model. You can modify the script to fit your needs. Note that we use three stages to train the model, as stated in the paper. The training dataset and training arguments may need to be changed for each stage.

We provide a fine-tuned checkpoint in HuggingFace:
- [Violet-yo/mt5-small-ft-Chinese-Braille](https://huggingface.co/Violet-yo/mt5-small-ft-Chinese-Braille)

## Evaluation
### Test Inference
We provide an example inference script. You can run it by:
```bash
python test_inference_simp.py
```
The script will load the fine-tuned model and translate the input text to braille. You can modify the input text in the script.

### Evaluate on the Validation and Test Set
You can get the score on the validation and test set by running:
```bash
bash run_translation_evaluation.sh
```

## Contact
If you have any questions about out project, please feel free to emial to [ayw34@cornell.edu](mailto:ayw34@cornell.edu).


## Citation
```
@misc{wu2024visionbrailleendtoendtoolchinese,
      title={Vision-Braille: An End-to-End Tool for Chinese Braille Image-to-Text Translation}, 
      author={Alan Wu and Ye Yuan and Ming Zhang},
      year={2024},
      eprint={2407.06048},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2407.06048}, 
}
```
