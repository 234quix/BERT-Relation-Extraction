#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 17:40:16 2019

@author: weetee
"""
from src.tasks.trainer import train_and_fit
from src.tasks.infer import infer_from_trained, FewRel
import logging
# from absl import logging

from argparse import ArgumentParser
import pdb
import sh


'''
This fine-tunes the BERT model on SemEval task 
'''
# logger = logging.getLogger('simple_example')
# logger.setLevel(logging.INFO)
# # create file handler which logs even debug messages
# fh = logging.FileHandler('spam.log')
# fh.setLevel(logging.INFO)
# # create console handler with a higher log level
# ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
# # create formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
# # add the handlers to logger
# logger.addHandler(ch)
# logger.addHandler(fh)

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                               level=logging.INFO,
                               handlers=[logging.FileHandler("{0}".format('mylogfile'), mode='a'),logging.StreamHandler()])

logger = logging.getLogger('__name__')


# logger.info('hello') 
# exit(1)
# import IPython ; IPython.embed() ; exit(1)

# logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', \
                    # datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
# logger = logging.getLogger('__file__')

if __name__ == "__main__":
    parser = ArgumentParser()
    # parser.add_argument("--task", type=str, default='semeval', help='semeval, fewrel')
    parser.add_argument("--task", type=str, default='semeval_debug', help='semeval, fewrel, semeval_debug')
    parser.add_argument("--train_data", type=str, default='./data/SemEval2010_task8_all_data_debug/SemEval2010_task8_training/TRAIN_FILE.TXT', \
                        help="training data .txt file path, \
                        ./data/SemEval2010_task8_all_data/SemEval2010_task8_training/TRAIN_FILE.TXT,\
                        ./data/SemEval2010_task8_all_data_debug/SemEval2010_task8_training/TRAIN_FILE.TXT")
    parser.add_argument("--test_data", type=str, default='./data/SemEval2010_task8_all_data/SemEval2010_task8_testing_keys/TEST_FILE_FULL.TXT', \
                        help="test data .txt file path")
    parser.add_argument("--use_pretrained_blanks", type=int, default=0, help="0: Don't use pre-trained blanks model, 1: use pre-trained blanks model")
    parser.add_argument("--num_classes", type=int, default=19, help='number of relation classes')
    parser.add_argument("--batch_size", type=int, default=32, help="Training batch size")
    parser.add_argument("--gradient_acc_steps", type=int, default=1, help="No. of steps of gradient accumulation")
    parser.add_argument("--max_norm", type=float, default=1.0, help="Clipped gradient norm")
    parser.add_argument("--fp16", type=int, default=0, help="1: use mixed precision ; 0: use floating point 32") # mixed precision doesn't seem to train well
    parser.add_argument("--num_epochs", type=int, default=10, help="No of epochs")
    parser.add_argument("--lr", type=float, default=0.00005, help="learning rate")
    # parser.add_argument("--model_no", type=int, default=2, help='''Model ID: 0 - BERT\n
    #                                                                         1 - ALBERT,\
    #                                                                         2 - SCIBERT''')
    parser.add_argument("--model_no", type=int, default=1, help='''Model ID: 0 - BERT\n
                                                                            1 - ALBERT,\
                                                                            2 - SCIBERT''')
    # parser.add_argument("--model_size", type=str, default='allenai/scibert_scivocab_uncased', help="For BERT: 'bert-base-uncased', \
    #                                                                                             'bert-large-uncased',\
    #                                                                                 For ALBERT: 'albert-base-v2',\
    #                                                                                             'albert-large-v2',\
    #                                                                                 For SCIBERT: 'allenai/scibert_scivocab_uncased'")
    parser.add_argument("--model_size", type=str, default='albert-base-v2', help="For BERT: 'bert-base-uncased', \
                                                                                                'bert-large-uncased',\
                                                                                    For ALBERT: 'albert-base-v2',\
                                                                                                'albert-large-v2',\
                                                                                    For SCIBERT: 'allenai/scibert_scivocab_uncased'")
    parser.add_argument("--train", type=int, default=1, help="0: Don't train, 1: train")
    parser.add_argument("--infer", type=int, default=1, help="0: Don't infer, 1: Infer")
    
    args = parser.parse_args()
    
    if (args.train == 1) and (args.task != 'fewrel'):
        net = train_and_fit(args)
        
    if (args.infer == 1) and (args.task != 'fewrel'):
        inferer = infer_from_trained(args, detect_entities=True)
        test = "The surprise [E1]visit[/E1] caused a [E2]frenzy[/E2] on the already chaotic trading floor."
        inferer.infer_sentence(test, detect_entities=False)
        test2 = "After eating the chicken, he developed a sore throat the next morning."
        inferer.infer_sentence(test2, detect_entities=True)
        
        while True:
            sent = input("Type input sentence ('quit' or 'exit' to terminate):\n")
            if sent.lower() in ['quit', 'exit']:
                break
            inferer.infer_sentence(sent, detect_entities=False)
    
    if args.task == 'fewrel':
        fewrel = FewRel(args)
        meta_input, e1_e2_start, meta_labels, outputs = fewrel.evaluate()
