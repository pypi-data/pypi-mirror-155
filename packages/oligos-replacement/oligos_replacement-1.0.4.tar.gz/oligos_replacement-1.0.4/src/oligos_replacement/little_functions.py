def startend(num_oligo, dataframe):
    start = dataframe['start'][num_oligo] - 1
    end = dataframe['end'][num_oligo]
    return start, end


def oligo_positions(line, dataframe):  # trouve les positions des oligos du chromosome de line
    L = []
    for k in range(len(dataframe)):
        if dataframe['chr'][k] in line:
            L.append(k)
    return L


def names_csv_wrong(dataframe):
    line = list(dataframe.columns)
    if 'chr' not in line or 'start' not in line or 'end' not in line or \
            'sequence_modified' not in line or 'sequence_original' not in line:
        return True


def not_in_oligo(position_art, reads_size, line, startart, endart, oligos_positionsart):
    if oligos_positionsart == [] \
            or position_art < startart - 2 * len(line) - reads_size \
            or position_art > endart + 2 * len(line) + reads_size:
        return True


def add_chr_artififial(artificial, output_genome):
    with open(output_genome, 'r') as new_genome:
        new_genome.readline()
        line = new_genome.readline()
        long = len(line) - 1

    n = 0
    with open(output_genome, 'a') as new_genome:
        new_genome.write(">chr_artificial  " + '(' + str(len(artificial)) + ' bp)' + "\n")
        while n < len(artificial):
            if n + long > len(artificial):
                new_genome.write(artificial[n:])
                new_genome.write('\n')
                n += long
            else:
                new_genome.write(artificial[n:n + long] + '\n')
                n += long
