#!/bin/bash

model_dir=models/wmt15-de-en.model
data_dir=data/wmt15-de-en

src_vocab=${data_dir}/en-vocab.50k.txt
tgt_vocab=${data_dir}/de-vocab.50k.txt
src_emb=${data_dir}/en-embedding.emb
tgt_emb=${data_dir}/de-embedding.emb
src=${data_dir}/newstest2013.en
tgt=${data_dir}/newstest2013.de
src_trans=${data_dir}/news-commentary-v10.de-en.en
tgt_trans=${data_dir}/news-commentary-v10.de-en.de
src_test=${data_dir}/newstest2013.en
tgt_test=${data_dir}/newstest2013.de

src_test_trans=${data_dir}/newstest2013.en.m1
tgt_test_trans=${data_dir}/newstest2013.de.m1

timestamp=$(date +%s)
score_file=${model_dir}/scores-${timestamp}.txt

> ${score_file}

score_test()
{
    echo ${src_test_trans} >> ${score_file}
    perl multi-bleu.perl ${tgt_test} < ${src_test_trans} >> ${score_file}
    echo ${tgt_test_trans} >> ${score_file}
    perl multi-bleu.perl ${src_test} < ${tgt_test_trans} >> ${score_file}
}

score_test

for i in $(seq 2 5); do
    # Train for one epoch.
    python ref/training.py \
           --model_dir ${model_dir} \
           --src ${src} \
           --tgt ${tgt} \
           --src_trans ${src_trans} \
           --tgt_trans ${tgt_trans} \
           --src_vocab ${src_vocab} \
           --tgt_vocab ${tgt_vocab} \
           --src_emb ${src_emb} \
           --tgt_emb ${tgt_emb}

    # Evaluate on test files.
    src_test_trans=${src_test}.m${i}
    tgt_test_trans=${tgt_test}.m${i}

    python ref/inference.py \
           --model_dir ${model_dir} \
           --src ${src_test} \
           --tgt ${tgt_test} \
           --src_vocab ${src_vocab} \
           --tgt_vocab ${tgt_vocab} \
           --direction 1 \
           > ${src_test_trans}
    python ref/inference.py \
           --model_dir ${model_dir} \
           --src ${src_test} \
           --tgt ${tgt_test} \
           --src_vocab ${src_vocab} \
           --tgt_vocab ${tgt_vocab} \
           --direction 2 \
           > ${tgt_test_trans}

    score_test

    # Translate training data.
    src_trans=${src}.m${i}
    tgt_trans=${tgt}.m${i}

    python ref/inference.py \
           --model_dir ${model_dir} \
           --src ${src} \
           --tgt ${tgt} \
           --src_vocab ${src_vocab} \
           --tgt_vocab ${tgt_vocab} \
           --direction 1 \
           > ${src_trans}
    python ref/inference.py \
           --model_dir ${model_dir} \
           --src ${src} \
           --tgt ${tgt} \
           --src_vocab ${src_vocab} \
           --tgt_vocab ${tgt_vocab} \
           --direction 2 \
           > ${tgt_trans}
done
