from bed_assembly import bed_assembly
from little_functions import names_csv_wrong, startend, oligo_positions, not_in_oligo, add_chr_artififial
from oligofile_correction import oligo_correction


def replacement(input_genome, input_oligos, output_genome, bed_path, reads_sizes):
    oligos = oligo_correction(input_oligos)
    if names_csv_wrong(oligos):
        return 'Error : the columns names of the csv file are not correct, please check README file'
    position = 0
    position_art = 0
    start, end = startend(0, oligos)
    startart, endart = startend(0, oligos)
    reads_size = reads_sizes
    artificial = ''
    with open(output_genome, 'w') as new_genome:
        new_genome.write('')
    with open(input_genome, 'r') as genome:
        for line in genome:
            if line[0] == '>':
                position = 0
                position_art = 0
                position_oligo = 0
                oligos_positions = oligo_positions(line, oligos)
                oligos_positionsart = oligo_positions(line, oligos)
                k = 0
                kart = 0
                if oligos_positions != [] and oligos_positionsart != []:
                    start, end = startend(oligos_positions[k], oligos)
                    startart, endart = startend(oligos_positionsart[kart], oligos)
                with open(output_genome, 'a') as new_genome:
                    new_genome.write(line)

            elif not_in_oligo(position_art, reads_size, line, startart, endart, oligos_positionsart):
                with open(output_genome, 'a') as new_genome:
                    new_genome.write(line)
                position += len(line) - 1
                position_art += len(line) - 1

            else:
                for ch in line:
                    if position_art in range(startart - reads_size, endart + reads_size) and ch != '\n':
                        artificial += ch
                        position_art += 1

                        if position_art == endart + reads_size \
                                and kart < len(oligos_positionsart) - 1:

                            kart += 1
                            startart, endart = startend(oligos_positionsart[kart], oligos)

                    elif ch != '\n':
                        position_art += 1

                    if position in range(start, end) and ch != '\n':

                        with open(output_genome, 'a') as new_genome:
                            new_genome.write(oligos['sequence_modified'][oligos_positions[k]][position_oligo])

                        position_oligo += 1
                        position += 1
                        if position == end and k < len(oligos_positions) - 1:
                            position_oligo = 0
                            k += 1
                            start, end = startend(oligos_positions[k], oligos)

                    else:
                        with open(output_genome, 'a') as new_genome:
                            new_genome.write(ch)
                            if ch in ['A', 'T', 'G', 'C', 'N', 'a', 't', 'g', 'c', 'n']:
                                position += 1

    bed_assembly(oligos, reads_sizes, bed_path)

    if line[-1] != '\n':
        with open(output_genome, 'a') as new_genome:
            new_genome.write('\n')
    add_chr_artififial(artificial, output_genome)
