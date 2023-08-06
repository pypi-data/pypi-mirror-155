from little_functions import startend


def chr_name_bed(oligos, num_oligo):
    name = ''
    for ch in oligos['chr'][num_oligo]:
        if ch == ' ':
            return name
        name += ch


def bed_assembly(oligos, reads_sizes, bedpath):
    n_cum = 1
    with open(bedpath, 'w') as bed:
        # genome
        for k in range(len(oligos)):
            start, end = startend(k, oligos)
            start += 1
            n = len(oligos['sequence_original'][k])
            # flank 5'

            if start == 1:
                pass
            elif start - reads_sizes <= 0:
                bed.write(chr_name_bed(oligos, k) + '\t1\t' + str(start) + '\toligo ' +
                          str(k) + " flank 5'" + '\n')
            elif k > 0 and start - reads_sizes < oligos['end'][k - 1]:
                pass
            else:
                bed.write(chr_name_bed(oligos, k) + '\t' + str(start - reads_sizes) + '\t' +
                          str(start-1) + '\toligo ' + str(k) + " flank 5'" + '\n')
                n_cum += reads_sizes

            # oligo
            bed.write(chr_name_bed(oligos, k) + '\t' + str(start) + '\t' +
                      str(end) + '\toligo ' + str(k) + '\n')

            n_cum += n

            # flank 3'
            if k + 1 != len(oligos) and end + reads_sizes >= oligos['start'][k + 1]\
                    and chr_name_bed(oligos, k) == chr_name_bed(oligos, k+1):
                bed.write(chr_name_bed(oligos, k) + '\t' + str(end+1) + '\t' +
                          str(oligos['start'][k + 1]-1) + '\toligo ' + str(k) + " flank 3'" + '\n')
                bed.write(chr_name_bed(oligos, k) + '\t' + str(end+1) + '\t' +
                          str(oligos['start'][k + 1]-1) + '\toligo ' + str(k+1) + " flank 5'" + '\n')

                n_cum += reads_sizes
            else:
                bed.write(chr_name_bed(oligos, k) + '\t' + str(end+1) + '\t' +
                          str(end + reads_sizes) + '\toligo ' + str(k) + " flank 3'" + '\n')
                n_cum += reads_sizes

        # artificial

        n_cum = 1
        for k in range(len(oligos)):
            start, end = startend(k, oligos)
            start += 1
            n = len(oligos['sequence_original'][k])

            # flank 5'
            if start == 1:
                pass
            elif start - reads_sizes < 0:
                bed.write('chr_artificial' + '\t1\t' + str(start-1) + '\toligo ' + str(k) + " flank 5'" + '\n')
                n_cum += start
            elif k > 0 and start - reads_sizes < oligos['end'][k - 1]:
                pass
            else:
                bed.write('chr_artificial' + '\t' + str(n_cum) + '\t' +
                          str(n_cum + reads_sizes - 1) + '\toligo ' + str(k) + " flank 5'" + '\n')
                n_cum += reads_sizes

            bed.write('chr_artificial' + '\t' + str(n_cum) + '\t' +
                      str(n_cum + n - 1) + '\toligo ' + str(k) + '\n')
            n_cum += n

            if k + 1 != len(oligos) and end + reads_sizes >= oligos['start'][k + 1]\
                    and chr_name_bed(oligos, k) == chr_name_bed(oligos, k+1):
                new_reads_sizes = reads_sizes
                while k + 1 != len(oligos) and end + new_reads_sizes >= oligos['start'][k + 1]:
                    new_reads_sizes -= 1
                bed.write('chr_artificial' + '\t' + str(n_cum) + '\t' +
                          str(n_cum + new_reads_sizes - 1) + '\toligo ' + str(k) + " flank 3'" + '\n')
                bed.write('chr_artificial' + '\t' + str(n_cum) + '\t' +
                          str(n_cum + new_reads_sizes - 1) + '\toligo ' + str(k+1) + " flank 5'" + '\n')
                n_cum += new_reads_sizes

            else:
                bed.write('chr_artificial' + '\t' + str(n_cum) + '\t' +
                          str(n_cum + reads_sizes - 1) + '\toligo ' + str(k) + " flank 3'" + '\n')
                n_cum += reads_sizes
