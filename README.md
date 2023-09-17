Copyright © 2022-2023 Sophie Colette. All Rights Reserved.

## Code accompanying my Master's thesis in Bioinformatics

**Title: Machine learning for organism growth temperature prediction and application of resampling methods to improve imbalanced data**

Promotor: prof. Vera van Noort

Supervisor: Jaldert François

Each folder contains the code for part of the workflow:

1. `Mining`: Web mining and integration with existing OGT databases
2. `Database QC`: Quality assessment of the databases
3. `Genome retrieval`: Extracting genomes for the species with available growth temperature
4. `Genome Annotation`: Proteome predictions with Prokka and Augustus
5. `Stability`: Feature stability analyses for the AA descriptors on protein and proteome level
6. `Data Analysis`: PCA and correlation analyses
7. `Embeddings`: Extraction of ProtTrans and UniProt embeddings
8. `Modelling`: linear regression models + XGBoost, SVR and RF both without (random split and phylogenetic split) and with resampling 
9. `Agreement statistics`: Comparison of the predicted proteomes with UniProt reference proteomes


(currently in progress): A more up-to-date version with additional clarifications is available at:
https://github.com/SC-Git1/OGTpredModels
