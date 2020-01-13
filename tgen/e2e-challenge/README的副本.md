Range Voting on TGen Baseline
=======================================

This project largely relies on [TGen](https://github.com/UFAL-DSG/tgen), [e2e_metrics](https://github.com/tuetschek/e2e-metrics), and the paper [Leveraging sentence similarity in natural language generation: Improving beam search using range voting](https://arxiv.org/abs/1908.06288), since it reimplements the range voting approach to the TGen baseline. 

## TGen outputs

1. Make sure to run in an environment that has all dependencies for tgen and e2e-metrics installed. Please refer to corresponding READMEs for further instructions. Train tgen.

2. Convert test data

   ```
   ./convert.py -a name,near -n -m new-data/testset_w_refs.csv test
   ```

3. For each beam size, repeat step 3 to 6. Set beam size in /tgen/e2e-challenge/config/config.yaml

4. Generate baseline outputs with the orginal tgen codebase 

   ```
   ../run_tgen.py seq2seq_gen -w baseline_{beam_size}.txt -a input/test-abst.txt \
       model.pickle.gz input/test-das.txt
   ./postprocess/postprocess.py baseline_{beam_size}.txt
   ```
   
5. Switch to my tgen codebase and generate output for range voting

   ```
   ../run_tgen.py seq2seq_gen -b 2 -w output_{beam_size}.txt -a input/test-abst.txt \
       model.pickle.gz input/test-das.txt  
   # do not post process the output at this point
   ```
   
6. Generate overlap, precision, and lstm results. Output will be written to 3 files, overlap_res.txt, precision_res.txt, and lstm_res.txt. They can be renamed to overlap_res_{beam_size}.txt, precision_res_{beam_size}.txt, and lstm_res_{beam_size}.txt and postprocessed.

   ```
   python range_voting.py output_{beam_size}.txt prob_{beam_size}.txt lstm_{beam_size}.txt
   # clear tmp files
   rm prob.txt
   rm lstm.txt
   ./postprocess/postprocess.py {method}_res_{beam_size}.txt
   ```

## E2E-metric evaluation

1. Prepare tsv files (baseline.tsv, precision.tsv, overlap.tsv, lstm.tsv) with corresponding MRs and outputs in the example-inputs folder.

2. Run the evaluation script and store the results in corresponding files

   ```
   ./measure_scores.py example-inputs/testset_w_refs.tsv example-inputs/baseline_{beam_size}.tsv -p |& tee output/baseline_{beam_size}.txt
   ./measure_scores.py example-inputs/testset_w_refs.tsv example-inputs/precision_{beam_size}.tsv -p |& tee output/precision_{beam_size}.txt
   ./measure_scores.py example-inputs/testset_w_refs.tsv example-inputs/overlap_{beam_size}.tsv -p |& tee output/overlap_{beam_size}.txt
   ./measure_scores.py example-inputs/testset_w_refs.tsv example-inputs/lstm_{beam_size}.tsv -p |& tee output/lstm_{beam_size}.txt
   ```

3. Run my evaluation script to add additional scores to the corresponding files with the following arguments.

   ```
   python eval.py example-inputs/baseline_res_{beam_size}.txt output/baseline_{beam_size}.txt example-inputs/precision_res_{beam_size}.txt output/precision_{beam_size}.txt example-inputs/overlap_res_{beam_size}.txt output/overlap_{beam_size}.txt example-inputs/lstm_res_{beam_size}.txt output/lstm_{beam_size}.txt
   
   ```