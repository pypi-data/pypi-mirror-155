# Oligos replacement : a subproject that replaces olds oligo sequences by those created for ssDNA HiC



***

## Description  
This project is a subproject to analyze the sequencing data generated after the ssDNA HiC Capture
protocol. It generates the a genome from the original genome and the new oligos designed in the
protocol. The new genome is a copy of the original exepted for the oligos regions, the sequence is 
replaced by the oligos sequence. Also, it adds a new chromosome named ```chr_artificial```
which is a concatenation of the original sequence of the oligos with their flanking regions
(defined by the user). To finish, the program creates a ```.bed``` file that contains all the 
coordinates of the oligos in the new genome and in the artificial chromosome and indicates if
the sequence is a flanking region or the oligo itself.

## Dependencies  
Python3 dependencies :
- ```pandas```
- ```Bio.Seq```


## Installation

The easiest way to install oligos replacement is using pip : 
```
pip3 install oligo_replacement 
```

## Run the program

Once installed, you can run the main function ```replacement``` 
which takes five arguments :

- The original genome path
- The oligos file path
- An output path where will be created the new genome
- An output path where will be created the ```.bed``` file
- The lengh of the flanking region you want

## Formats and conventions

This projects has to be used with the following instructions to work correctly.

### Files formats :

- Genomes : ```fasta```
- Oligos file : ```csv```

### Oligo file structure :

This file has to contained at least 6 columns with the **precises** headers below :

| chr | start | stop | orientation | sequence_original | sequence_modified |
|-----|-------|------|-------------|-------------------|-------------------|

- [ ] In the```chr``` column, it has to be the entire line of the chromome description in the fasta file without 
the chevron ```>```

- [ ] In the ```start``` column, the position of the first nucleotide (included) of the oligo 
(the first nucleotide of the chromosome is the number 1)

- [ ] In the ```end``` column, the position of the last nucleotide (included) of the oligo

- [ ] In the ```orientation``` column, the a 'C' for Crick and 'W' for Watson

- [ ] In the ```sequence_original``` column, the original sequence of the oligo

- [ ] In the ```sequence_original``` column, the modified sequence of the oligo

The first oligo is the number 0.

### ```.bed``` file structure

The ```.bed``` file generated is a ```bed4```. 

- [ ] The first column indicates the chromosome name (the classic genome or the
artificial chromosome)
- [ ] The second column contains the position of the first nucleotide (included)
- [ ] The third column contains the position of the last nucleotide (included)
- [ ] The fourth column is ```oligo x``` with ```x``` the oligo number and followed by ```flank 5'``` or ```flank 3'```
  (if the flanking sequence is in 3' or 5' side) and nothing after if the sequence is 
the oligo itself.
  