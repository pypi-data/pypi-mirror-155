from Bio.Seq import Seq
import pandas as pd
pd.options.mode.chained_assignment = None


def oligo_correction(input_oligos):
    oligos = pd.read_csv(input_oligos, sep=",")
    oligos.columns = [oligos.columns[k].lower() for k in range(len(oligos.columns))]

    oligos = oligos.sort_values(by=['chr', 'start'])
    for k in range(len(oligos)):

        if oligos['orientation'][k] == 'C':
            oligos['orientation'][k] = 'W'

            original = Seq(oligos['sequence_original'][k])
            oligos['sequence_original'][k] = str(original.reverse_complement())

            modified = Seq(oligos['sequence_modified'][k])
            modified = modified.upper()
            oligos['sequence_modified'][k] = str(modified.reverse_complement())

        elif oligos['orientation'][k] == 'W':
            modified = Seq(oligos['sequence_modified'][k])
            modified = modified.upper()
            oligos['sequence_modified'][k] = str(modified)

    return oligos
