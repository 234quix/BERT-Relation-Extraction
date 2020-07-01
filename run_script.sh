# Run Albert in with debug data
#python main_task.py
# Run Albert with normal data
#python main_task.py --task semeval --train_data ./data/SemEval2010_task8_all_data/SemEval2010_task8_training/TRAIN_FILE.TXT
# Run SciBert with normal data
python main_task.py --model_no 2 --model_size allenai/scibert_scivocab_uncased --task semeval --train_data ./data/SemEval2010_task8_all_data/SemEval2010_task8_training/TRAIN_FILE.TXT
