DataBuffet is a tool and framework for automatically loading heterogeneous ML datasets.

[**Getting Started**](⚡️-Quickstart)
| [**What is DataBuffet?**](💡-Databuffet-in-short)
| [**What is it solving?**](❗️-Problem-which-we’re-trying-to-solve)
| [**Repo structure**](🏗-Structure-of-the-repo)
| [**Report**](📄-Report)

# ⚡️ Quickstart

To use our framework, you just have to install it via pip and then you can load a dataset like below:

```python
pip install databuffet
```

```python
import databuffet

# load the dataset and output a table
out_df = databuffet.defaultDatasetLoader.loadDataset("./path/to/dateset/")

# split the output table into 3 smaller tables based on the filename
train_df = out_df[out_df["db_table_name"] == "train.tsv"]
test_df = out_df[out_df["db_table_name"] == "test.tsv"]
validation_df = out_df[out_df["db_table_name"] == "validation.tsv"]

### now you can use the date for you ML model
```

# 💡 Databuffet in short

The field of machine learning has recently gained much traction and interest. But to even begin working on a machine learning task one needs to first load the dataset from disk into memory. Usually, this entails writing some code for parsing and loading the data, which in itself isn't innovative, but still needs to be adapted to each particular dataset. To make this part, loading of a dataset, as seamless as possible, we present: (1) a framework and (2) an initial tool built with our framework which strives to automatically load the dataset and output a table that is compatible with a `pandas.DataFrame`.

The aim of our framework is to be able to load any dataset, but as an initial showcase, we build our tool with a focus on loading datasets that primarily contain CSV/TSV files. For such datasets, our tool achieves a success rate of 45%. The performance evaluation was done using a dataset corpus of over 600 real-world datasets used for ML tasks. This initial tool is currently in its infancy and should serve more as a showcase of the capabilities of our framework, rather than a showcase of its performance. Lastly, our framework allows for easy extensibility of the tool and as such, we hope it will grow over time to be able to load almost all datasets.

# ❗️ Problem which we’re trying to solve

Depending on the task for which they are used, machine learning datasets can consist of a variety of different file types (images, text files, JSON files, tables, etc.) and their combinations. Because of this and because there isn't a widely accepted standard on how to store or format datasets, one can't draw any conclusions on what data an arbitrary dataset contains or into which representation its data should be loaded. This in turn makes working with an unfamiliar dataset hard as one needs to first figure out what the dataset contains, how the data is formatted and how it should be loaded before one can actually use it for machine learning related tasks. Usually this entails writing some boilerplate code for parsing and loading of the data which isn't innovative, but still needs to be adapted to each particular dataset and its structure.

<p align="center">
    <img src="./images/sample_dataset.png" alt="Sample dataset" height="300"/>
</p>

To give a concrete example, let’s say that you want to load the dataset in the above figure. To do that you would first have to explore it in your file explorer, see what is relevant and the write some glue code like the following:

<p align="center">
    <img src="./images/glue_code.png" alt="Glue code" height="250"/>
</p>

Exactly this tedious part, loading of an unfamiliar dataset, we're trying to automate so that one can readily use any dataset without wasting time on such menial tasks.

# 🏗 Structure of the repo

- /databuffet

    Main code for the tool and framework.

    - /databuffet/transformers.py

        Main class for the transformers which transform the dataset tree and dataset table. Furthermore, contains some initial transformers.

    - /databuffet/dataset_tree.py

        Functions which build the dataset tree. Furthermore, tree helper functions which make modifying dataset trees much easier and, by doing so, make creating new transformers much easier.

    - /databuffet/dataset_tree_nodes.py

        Main classes which are used in the dataset tree. Namely, one which represents filesystem items and another which represents folders.

    - /databuffet/dataset_loaders.py

        Main class for the dataset loaders (”compilers” for datasets). Furthermore, contains the initial default dataset loader which is composed of the initial transformers.

    - /databuffet/file_loaders.py

        Functions which are used to load different filetypes from the filesytem into Python objects.

- /appendix

    Contains the code used to download the 600+ datasets, the code to do the performance evaluation and the code used for the demo in the report.

- /tests

    Tests used to evaluate the correctness of the framework.


# 📄 Report

BataBuffet was created as part of a bachelor’s thesis by Filip Jaksic at ETH Zurich under the supervision of Bojan Karlas and Prof. Dr. Ce Zhang who represent the DS3Lab at ETH Zurich.

The full report can be found here:

[DataBuffet - Towards a Tool for Automatically Loading Heterogeneous ML Datasets.pdf](./DataBuffet%20-%20Towards%20a%20Tool%20for%20Automatically%20Loading%20Heterogeneous%20ML%20Datasets.pdf)
