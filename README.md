# reticulatus
A long snake for a long assemblies

## How to drive this thing

### (1) Setup the environment

```
conda env create --name reticulatus --file environments/base.yaml
conda activate reticulatus
```

Initalise which pipeline you want. It will almost always be `Snakefile-base` for the time being. Run `Snakefile-full`to replicate our mock community pipeline.

```
cp Snakefile-base Snakefile
```

### (2) Write your configuation

```
cp config.yaml.example config.yaml
```

Replace the YAML keys as appropriate. Keys are:

| Key | Type | Description | 
|-----|------|-------------|
| `dehumanizer_database_root` | Path | empty directory in which to download the dehumanizer references (requires ~8.5GB), you can ignore this if you're not going to remove contigs assigned as human by `kraken2` |
| `kraken2_database_root` | Path | path to pre-built kraken2 database (*i.e.* the directory containing the `.k2d` files), or the path to a directory in which to `wget` a copy of our 30GB [microbial database](https://lomanlab.github.io/mockcommunity/mc_databases.html). **If the database already exists, you must** `touch k2db.ok` in this directory or **bad things** will happen |
| `slack_token` | str | if you want to be bombarded with slack messages regarding the success and failure of your snakes, insert a suitable bot API token here |
| `slack_channel` | str | if using a `slack_token`, enter the name of the channel to send messages, including the leading `#` |
| `cuda` | boolean | set to `False` if you do not want GPU-acceleration and `True` if you have the means to go very fast (*i.e.* you have a CUDA-compatible GPU) |
| `medaka_env` | URI | path to a singularity image (simg) or sandbox container to run medaka (GPU) |

### (3) Tell reticulatus about your reads

```
cp reads.cfg.example reads.cfg
```

For each sample you have, add a tab delimited line with the following fields: 

| Key | Type | Description | 
|-----|------|-------------|
| `sample_name` | str | a unique string that can be used to refer to this sample/readset later |
| `ont` | Path* | path to your long reads |
| `i0` | Path* | path to your single-pair short reads for this sample, otherwise you can just set to `-` |
| `i1` | Path* | path to your left paired-end short reads |
| `i2` | Path* | path to your right paired-end short reads |
| `*` | - | an arbitrary delimiter that has no purpose |
||| feel free to add your own columns for metadata here, fill your boots, reticulatus doesn't care |

**\*** You can pre-process reads by modfying their file path as follows:

| Option | Syntax | Description | 
|--------|--------|-------------|
| Remove duplicates | myreads.**rmdup**.fq.gz | remove reads with a duplicate sequence header (to fix occasional duplicate reads arising from basecalling) |
| Subset reads | myreads.**subset-N**.fq.gz | select a random subsample of `N%` (with integer `N` between 1-99) |
| Merge reads | /path/to/merged/reads/:myreads.fq.gz,myotherreads.fq.gz,... | a root path for merged reads, followed by a colon and a comma delimited list of files to `cat` together, the filename will be chosen automatically and you should not be upset by this |

Pre-processing can be chained, for example: `myreads.rmdup.subset-25.fq.gz`, will remove sequence name duplicates and take 25% of the result. You may also use this syntax to pre-process files for merging. Reticulatus will work out what needs to be done to generate the new read files, and will only need to do so once; even when you run the pipeline again in the future.
The processed reads will be written to the same directory as the original reads. Once this has been done, you can delete the original reads yourself, if you'd like.

**Important** If you're using the GPU, you must ensure the directories that contain your reads are bound to the singularity container with `-B` in `--singularity-args`, use the same path for inside as outside to make things easier.


### (4) Tell reticulatus about your plans

```
cp manifest.cfg.example manifest.cfg
```

For each pipe you want to run, add a tab delimited line with the following fields:

| Key | Type | Description | 
|-----|------|-------------|
| `uuid` | str | a unique identifier, it can be anything, it will be used as a prefix for every file generated by this pipe |
| `repolish` | str | a placeholder for a future feature, set to `-` for now |
| `samplename` | str | the read set to assemble and polish, it must be a key from `reads.cfg` |
| `spell` | str | the "spell" to configure your assembly and polishing, corresponding to a named configuration in `spellbook.py` |
| `polishpipe` | str | a minilanguage that determines the polishing strategy. strategies are of the format `<program>-<readtype>-<iterations>` and are chained with the `.` character. *e.g.* `racon-ont-4.medaka-ont-1.pilon-ill-1` will perform four rounds of iterative `racon` long-read polishing, followed by one round of medaka long-read polishing and finally one round of `pilon` short-read polishing. Currently the following polishers are supported: racon, medaka, pilon and dehumanizer. No polishing can be acheived by setting to `-`. |
| `medakamodel` | str | the option to pass to `medaka_consensus -m`, this corresponds to the model to use for medaka long-read polishing, it will depend on your ONT basecaller version |


### (5) Engage the pipeline

Run the pipeline with `snakemake`, you **must** specify `--use-conda` to ensure that
any tools that require a special jail (*e.g.* for `python2`) are run far, far away
from everything else.
Set `j` to the highest number of processes that you can fill with snakes before
your computer falls over.

#### Simple

```
snakemake -j <available_threads> --reason
```

#### Advanced (GPU)

Additionally you **must** specify `--use-singularity` to use containers **and** provide suitable `--singularity-args` to use the GPU and bind directories.
Don't forget to use the GPU, you must set the `cuda` key to True in `config.cfg`.

```
snakemake -j <available_threads> --reason --use-conda --use-singularity --singularity-args '--nv -B <dir_inside>:<dir_outside>' -k --restart-times 1
```

Using the GPU will accelerate the following steps:

* `polish_racon`: you will need a racon binary compiled with `CUDA`, for your system
* `polish_medaka`: you will need to specify an appropriate singularity container, or install medaka with GPU support yourself


## Housekeeping

Unless otherwise stated by a suitable header, the files within this repository are made available under the MIT license. If you use this pipeline, an acknowledgement in your work would be nice... Don't forget to [cite Snakemake](https://snakemake.readthedocs.io/en/stable/project_info/citations.html).
