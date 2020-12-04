# Matching Treatment and Control Groups

My goal is to estimate whether the amount of citations differ due to the mentioned-code-link behavior. However, endogeneity issues might occur if we do not account for unobservable properties that may both make the author share codes and also boost the paper's citation counts, such that he/she is a big name in a specific area. This endogeneity issue leads to a biased estimate of our interesting variable. Therefore, I plan to apply a matching approach before modeling in order to identify the causal effect. 

In particular, given a treated observation, a matching approach is to choose a most-similar observation from the untreated/control group, and then construct a pair of treated-control data. After matching, we can run regressions using a set of matched treated-control pairs, rather than the unmatched raw data, to measure the causal effect of the mentioned-code-link behaviors on paper citations.

In this project, I will focus on the following three componets: download and pre-process two large datasets (>10G) using python, conduct feature engineering, and apply the matching algorithm. 

The correpsonding `ipynb` files are listed below:
  - `step1_process_data.ipynb`
  - `step2_get_features.ipynb`
  - `step3_match.ipynb`
