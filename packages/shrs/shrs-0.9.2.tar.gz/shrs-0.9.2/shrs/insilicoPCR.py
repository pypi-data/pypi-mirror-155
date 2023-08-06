'''
Copyright (c) 2022 Masayuki TAKAHASHI

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

def insilicoPCR(args):
    """
    in silico PCR amplification algorithm.

    Parameters
    ----------
    args: ArgumentParser, class containing appropriate property as below
        input_file: Input file path (required)\n
        output: Output directory path (Make a new directory if the directory does not exist)\n
        size_limit: The upper limit of amplicon size\n
        process: The number of processes (sometimes the number of CPU core) used for analysis\n
        fasta: Output format. A FASTA file will be generated if you use this option.\n
        forward: The forward primer sequence used for amplification (required)\n
        reverse: The reverse primer sequence used for amplification (required)\n
        Single_file: Output format. One single FASTA-format file will be generated even if you input some separate FASTA files, when using this option with the '--fasta' option.\n
        Mismatch_allowance: The acceptable mismatch number\n
        Only_one_amplicon: Only one amplicon is outputted, even if multiple amplicons are obtained by PCR when you use this option.\n
        Position_index: The result has the information of the amplification position when this option is enabled.\n
        circularDNA: If there are some circular DNAs in the input sequences, use this option (default: n/a. It means all input sequences are linear DNA. When there are some circular DNA input sequences, type 'all', 'individually', 'n/a', or the file path of the text that specify which sequence is circularDNA, after the '--circularDNA' option. See Readme for more detailed information.)\n
            Text file example:\n
                Sequence_name1 circularDNA\n
                Sequence_name2 linearDNA\n
                Sequence_name3 linearDNA\n
                    ...\n
                Sequence_nameN circularDNA\n
        gene_annotation_search_range: The gene annotation search range in the GenBank-format file.\n
        Annotation: If the input sequence file is in GenBank format, the amplicon(s) is annotated automatically.\n
        warning: Shows all warnings when you use this option.\n

    Returns
    -------
    FASTA/CSV: Amplified sequence(s) FASTA format file (or CSV file)

    """
    import sys
    import os
    import re
    import warnings
    from functools import partial
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from tqdm import tqdm
    import math
    import itertools as it
    import numpy as np
    import pandas as pd
    from multiprocessing import Pool, get_context, cpu_count
    from shrslib.basicfunc import init_worker, read_sequence_file, circularDNA, check_input_file
    from shrslib.explore import PCR_amplicon
    from shrslib.multiprocessfunc import trim_seq_worker_process_all, trim_seq_worker_process_all_df, trim_seq_worker_process_single, trim_seq_worker_process_single_df, PCR_amplicon_with_progress_bar
    try:
        input_file = args.input_file
    except:
        sys.exit("Need a FASTA file or folder containing FASTA files after '-i '. \nPlease use '-h' or '--help' option if you would like to confirm usage.")
    if os.path.isfile(input_file):
        file_paths = [input_file]
    elif os.path.isdir(input_file):
        file_names = os.listdir(input_file)
        if input_file.endswith("/"):
            file_paths = [input_file+file_name for file_name in file_names]
        else:
            file_paths = [input_file+"/"+file_name for file_name in file_names]
        file_paths = [file_path for file_path in file_paths if os.path.isfile(file_path)]
        for file_path in file_paths:
            with open(file_path, "rt") as fin:
                Firstline = fin.readline()
                if np.logical_not(Firstline.startswith(">") | Firstline.startswith("LOCUS")):
                    print("There are some file(s) of which are not FASTA or Genbank in folder inputed. Please remove the file(s).")
                    sys.exit()
    else:
        sys.exit("Error: The input file/folder does not exist.")
    if args.output is not None:
        output_folder = args.output
        if not output_folder.endswith("/"):
            output_folder = output_folder+"/"
    else:
        output_folder = ""
    output_dataframe = args.fasta
    single_file = args.Single_file
    fwd = args.forward
    rev = args.reverse
    amplicon_size_limit = args.size_limit
    allowance = args.Mismatch_allowance
    Remain_all_amplicons = args.Only_one_amplicon
    Position_index = args.Position_index
    if args.Annotation:
        Feature = True
        Position_index = True
    else:
        Feature = False
    CPU = args.process
    if CPU is not None:
        if CPU > cpu_count():
            CPU = int(math.ceil(cpu_count()))
    else:
        if cpu_count() <= 3:
            CPU = int(1)
        elif cpu_count() <= 8:
            CPU = int(math.floor(cpu_count() / 2))
        elif cpu_count() <= 12:
            CPU = int(cpu_count() - 4)
        elif cpu_count() <= 24:
            CPU = int(math.floor(cpu_count() / 2) + 2)
        else:
            CPU = int(16)
    if args.circularDNA is not None:
        overlap_region = amplicon_size_limit
        if len(args.circularDNA) == 0:
            circular_index = check_input_file(file_paths, circular = "all")
        elif args.circularDNA[0].lower() == "all":
            circular_index = check_input_file(file_paths, circular = "all")
        elif args.circularDNA[0].lower() == "individually":
            circular_index = check_input_file(file_paths, circular = "individually")
        elif os.path.isfile(args.circularDNA[0]):
            circular_index = check_input_file(file_paths, circular = args.circularDNA[0])
        elif args.circularDNA[0].lower() == "n/a":
            overlap_region = 0
            circular_index = check_input_file(file_paths, circular = "n/a")
        else:
            print(" Specify the file path, 'all', 'individually' or 'n/a' after --circularDNA option.\n All input sequence(s) are analysed as circular DNA")
            circular_index = check_input_file(file_paths, circular = "all")
    else:
        overlap_region = 0
        circular_index = check_input_file(file_paths, circular = "n/a")
    distance = args.gene_annotation_search_range
    Warning_ignore = args.warning
    if Warning_ignore:
        warnings.simplefilter('ignore')
    Seq_no = []
    for file_path in file_paths:
        with open(file_path, "rt") as fin:
            read_FILE = fin.read()
            if read_FILE.startswith(">"):
                Seq_no += [read_FILE.count(">")]
            else:
                Seq_no += [1]
    annotation = {}
    if output_dataframe:
        Amplicon_Sequences = dict()
        if Remain_all_amplicons:
            if np.mean(Seq_no) > len(Seq_no):
                with tqdm(total = np.sum(Seq_no), desc = "Dataframe of amplified sequences making", leave = False, unit = "tasks", unit_scale = True) as pbar:
                    def Progressbar_update_alpha(Result):
                        pbar.update(Result[1])
                    for file_path in file_paths:
                        if Feature:
                            seq_dict = read_sequence_file(input = file_path, format = "genbank", Feature = True)[0]
                            annotation.update({key:seq_dict[key][1] for key in seq_dict})
                            seq_dict = {key:seq_dict[key][0] for key in seq_dict}
                        else:
                            seq_dict = read_sequence_file(file_path)[0]
                        Sequence_length_list = [np.min([amplicon_size_limit, seq_dict[key].sequence_length]) for key in seq_dict]
                        seq_dict = {key:circularDNA(sequence = seq_dict[key], overlap = int(np.min([overlap_region, seq_dict[key].sequence_length]))) if circular_index[key] else circularDNA(sequence = seq_dict[key], overlap = int(0)) for key in seq_dict}
                        if (CPU > 1):
                            with get_context("spawn").Pool(processes = min([CPU, len(seq_dict)]), initializer = init_worker) as pl:
                                try:
                                    if Position_index:
                                        Amplicon = [pl.apply_async(PCR_amplicon_with_progress_bar, kwds = {"forward": fwd, "reverse": rev, "template": seq, "Single_amplicon": False, "Sequence_Only": False, "amplicon_size_limit": limit, "allowance": allowance, "Warning_ignore": Warning_ignore}, callback = Progressbar_update_alpha) for limit, seq in zip(Sequence_length_list, seq_dict.values())]
                                    else:
                                        Amplicon = [pl.apply_async(PCR_amplicon_with_progress_bar, kwds = {"forward": fwd, "reverse": rev, "template": seq, "Single_amplicon": False, "Sequence_Only": True, "amplicon_size_limit": limit, "allowance": allowance, "Warning_ignore": Warning_ignore}, callback = Progressbar_update_alpha) for limit, seq in zip(Sequence_length_list, seq_dict.values())]
                                except KeyboardInterrupt:
                                    pl.terminate()
                                    pl.join()
                                    pl.close()
                                    print("\n\n --- Keyboard Interrupt ---")
                                    sys.exit("")
                                Amplicon = [amp.get()[0] for amp in Amplicon]
                        else:
                            if Position_index:
                                Amplicon = [(PCR_amplicon(forward = fwd, reverse = rev, template = seq, Single_amplicon = False, Sequence_Only = False, amplicon_size_limit = limit, allowance = allowance, Warning_ignore = Warning_ignore), pbar.update(1), ) for limit, seq in zip(Sequence_length_list, seq_dict.values())]
                            else:
                                Amplicon = [(PCR_amplicon(forward = fwd, reverse = rev, template = seq, Single_amplicon = False, Sequence_Only = True, amplicon_size_limit = limit, allowance = allowance, Warning_ignore = Warning_ignore), pbar.update(1), ) for limit, seq in zip(Sequence_length_list, seq_dict.values())]
                            Amplicon = [amp[0] for amp in Amplicon]
                        Amplicon = [[] if seq is None else seq for seq in Amplicon]
                        Amplicon = {name:amp for name, amp in zip(seq_dict.keys(), Amplicon)}
                        Amplicon_Sequences.update(Amplicon)
                    max_col = max([len(i) for i in Amplicon_Sequences.values()])
                    Amplicon_Sequences = {name:[seqs[i] if len(seqs) > i else np.nan for i in range(max_col)] for name, seqs in Amplicon_Sequences.items()}
                    Result = pd.DataFrame(Amplicon_Sequences).T
                    Result.columns = ["Amplicon_sequence_"+ str(i + 1) for i in range(max_col)]
            else:
                Result = dict()
                if Feature:
                    for file_path in file_paths:
                        seq_dict = read_sequence_file(input = file_path, format = "genbank", Feature = True)[0]
                        annotation.update({key:seq_dict[key][1] for key in seq_dict})
                        del seq_dict
                with get_context("spawn").Pool(processes = np.min([CPU, len(file_paths)]), initializer = init_worker) as pl:
                    try:
                        if Position_index:
                            Amplicons = list(tqdm(pl.imap(partial(trim_seq_worker_process_all_df, fwd = fwd, rev = rev, Sequence_Only = False, amplicon_size_limit = amplicon_size_limit, allowance = allowance, Warning_ignore = Warning_ignore, overlap_region = overlap_region, circular_index = circular_index), file_paths), total = np.sum(Seq_no), desc = "Dataframe of amplified sequences making", leave = False, unit = "tasks", unit_scale = True))
                        else:
                            Amplicons = list(tqdm(pl.imap(partial(trim_seq_worker_process_all_df, fwd = fwd, rev = rev, Sequence_Only = True, amplicon_size_limit = amplicon_size_limit, allowance = allowance, Warning_ignore = Warning_ignore, overlap_region = overlap_region, circular_index = circular_index), file_paths), total = np.sum(Seq_no), desc = "Dataframe of amplified sequences making", leave = False, unit = "tasks", unit_scale = True))
                    except KeyboardInterrupt:
                        pl.terminate()
                        pl.join()
                        pl.close()
                        print("\n\n --- Keyboard Interrupt ---")
                        sys.exit("")
                [Result.update(amplicon) for amplicon in Amplicons]
                Result = pd.DataFrame(Result).T
            if Position_index & Feature & (len(annotation) > 0):
                Amplicon_annotation = {}
                for i in range(len(Result.index)):
                    Gene = [[position for position in re.sub(r"[^0-9]+", " ", target).split(" ") if len(position) != 0] + [annotation[Result.index[i]][target]] for target in annotation[Result.index[i]].keys() if (Result.index[i] in annotation.keys())]
                    Amplicon_annotation.update({Result.index[i]:{"Annotation_of_amplicon_sequence_" + str(j + 1): ["{0}..{1}: {2}".format(g[0], g[1], g[2]) for g in Gene if (((int(g[0]) - int(distance)) <= np.abs(Result.iloc[i, j][0])) & ((int(g[1]) + int(distance)) >= np.abs(Result.iloc[i, j][0]))) | (((int(g[0]) - int(distance)) <= np.abs(Result.iloc[i, j][1])) & ((int(g[1]) + int(distance)) >= np.abs(Result.iloc[i, j][1]))) | (((int(g[0]) - int(distance)) >= np.abs(Result.iloc[i, j][0])) & ((int(g[1]) + int(distance)) <= np.abs(Result.iloc[i, j][1])))] if pd.notna(Result.iloc[i, j]) else np.nan for j in range(Result.shape[1])}})
                Amplicon_annotation = pd.DataFrame(Amplicon_annotation).T
                Result = pd.concat([Result, Amplicon_annotation],axis = 1)
        else:
            if np.mean(Seq_no) > len(Seq_no):
                with tqdm(total = np.sum(Seq_no), desc = "Dataframe of amplified sequences making", leave = False, unit = "tasks", unit_scale = True) as pbar:
                    def Progressbar_update_beta(Result):
                        pbar.update(Result[1])
                    for file_path in file_paths:
                        if Feature:
                            seq_dict = read_sequence_file(input = file_path, format = "genbank", Feature = True)[0]
                            annotation.update({key:seq_dict[key][1] for key in seq_dict})
                            seq_dict = {key:seq_dict[key][0] for key in seq_dict}
                        else:
                            seq_dict = read_sequence_file(file_path)[0]
                        Sequence_length_list = [np.min([amplicon_size_limit, seq_dict[key].sequence_length]) for key in seq_dict]
                        seq_dict = {key:circularDNA(sequence = seq_dict[key], overlap = int(np.min([overlap_region, seq_dict[key].sequence_length]))) if circular_index[key] else circularDNA(sequence = seq_dict[key], overlap = int(0)) for key in seq_dict}
                        if (CPU > 1):
                            with get_context("spawn").Pool(processes = min([CPU, len(seq_dict)]), initializer = init_worker) as pl:
                                try:
                                    if Position_index:
                                        Amplicon = [pl.apply_async(PCR_amplicon_with_progress_bar, kwds = {"forward": fwd, "reverse": rev, "template": seq, "Single_amplicon": True, "Sequence_Only": False, "amplicon_size_limit": limit, "allowance": allowance, "Warning_ignore": Warning_ignore}, callback = Progressbar_update_beta) for limit, seq in zip(Sequence_length_list, seq_dict.values())]
                                    else: 
                                        Amplicon = [pl.apply_async(PCR_amplicon_with_progress_bar, kwds = {"forward": fwd, "reverse": rev, "template": seq, "Single_amplicon": True, "Sequence_Only": True, "amplicon_size_limit": limit, "allowance": allowance, "Warning_ignore": Warning_ignore}, callback = Progressbar_update_beta) for limit, seq in zip(Sequence_length_list, seq_dict.values())]
                                except KeyboardInterrupt:
                                    pl.terminate()
                                    pl.join()
                                    pl.close()
                                    print("\n\n --- Keyboard Interrupt ---")
                                    sys.exit("")
                                Amplicon = [amp.get()[0] for amp in Amplicon]
                        else:
                            if Position_index:
                                Amplicon = [(PCR_amplicon(forward = fwd, reverse = rev, template = seq, Single_amplicon = True, Sequence_Only = False, amplicon_size_limit = limit, allowance = allowance, Warning_ignore = Warning_ignore), pbar.update(1), ) for limit, seq in zip(Sequence_length_list, seq_dict.values())]
                            else:
                                Amplicon = [(PCR_amplicon(forward = fwd, reverse = rev, template = seq, Single_amplicon = True, Sequence_Only = True, amplicon_size_limit = limit, allowance = allowance, Warning_ignore = Warning_ignore), pbar.update(1), ) for limit, seq in zip(Sequence_length_list, seq_dict.values())]
                            Amplicon = [amp[0] for amp in Amplicon]
                        Amplicon = ['' if seq is None else seq for seq in Amplicon]
                        if Position_index:
                            len_seqs = [len(seq[2]) if len(seq) > 1 else 0 for seq in Amplicon]
                        else:
                            len_seqs = [len(seq) for seq in Amplicon]
                        Amplicon = list(zip(Amplicon, len_seqs))
                        Amplicon = {name:amp for name, amp in zip(seq_dict.keys(), Amplicon)}
                        Amplicon_Sequences.update(Amplicon)
                    Result = pd.DataFrame(Amplicon_Sequences).T
                    Result.columns = ["Amplicon_sequence", "Length"]
            else:
                Result = dict()
                if Feature:
                    for file_path in file_paths:
                        seq_dict = read_sequence_file(input = file_path, format = "genbank", Feature = True)[0]
                        annotation.update({key:seq_dict[key][1] for key in seq_dict})
                        del seq_dict
                with get_context("spawn").Pool(processes = np.min([CPU, len(file_paths)]), initializer = init_worker) as pl:
                    try:
                        if Position_index:
                            Amplicons = list(tqdm(pl.imap(partial(trim_seq_worker_process_single_df, fwd = fwd, rev = rev, Sequence_Only = False, amplicon_size_limit = amplicon_size_limit, allowance = allowance, Warning_ignore = Warning_ignore, overlap_region = overlap_region, circular_index = circular_index), file_paths), total = np.sum(Seq_no), desc = "Dataframe of amplified sequences making", leave = False, unit = "tasks", unit_scale = True))
                        else:
                            Amplicons = list(tqdm(pl.imap(partial(trim_seq_worker_process_single_df, fwd = fwd, rev = rev, Sequence_Only = True, amplicon_size_limit = amplicon_size_limit, allowance = allowance, Warning_ignore = Warning_ignore, overlap_region = overlap_region, circular_index = circular_index), file_paths), total = np.sum(Seq_no), desc = "Dataframe of amplified sequences making", leave = False, unit = "tasks", unit_scale = True))
                    except KeyboardInterrupt:
                        pl.terminate()
                        pl.join()
                        pl.close()
                        print("\n\n --- Keyboard Interrupt ---")
                        sys.exit("")
                [Result.update(amplicon) for amplicon in Amplicons]
                Result = pd.DataFrame(Result).T
                Result.columns = ["Amplicon_sequence", "Length"]
            if Position_index & Feature & (len(annotation) > 0):
                Amplicon_annotation = {}
                for i in range(len(Result.index)):
                    Gene = [[position for position in re.sub(r"[^0-9]+", " ", target).split(" ") if len(position) != 0] + [annotation[Result.index[i]][target]] for target in annotation[Result.index[i]].keys() if (Result.index[i] in annotation.keys())]
                    Amplicon_annotation.update({Result.index[i]: ["{0}..{1}: {2}".format(g[0], g[1], g[2]) for g in Gene if (((int(g[0]) - int(distance)) <= np.abs(Result.loc[Result.index[i], 'Amplicon_sequence'][0])) & ((int(g[1]) + int(distance)) >= np.abs(Result.loc[Result.index[i], 'Amplicon_sequence'][0]))) | (((int(g[0]) - int(distance)) <= np.abs(Result.loc[Result.index[i], 'Amplicon_sequence'][1])) & ((int(g[1]) + int(distance)) >= np.abs(Result.loc[Result.index[i], 'Amplicon_sequence'][1]))) | (((int(g[0]) - int(distance)) >= np.abs(Result.loc[Result.index[i], 'Amplicon_sequence'][0])) & ((int(g[1]) + int(distance)) <= np.abs(Result.loc[Result.index[i], 'Amplicon_sequence'][1])))] if pd.notna(Result.loc[Result.index[i], 'Amplicon_sequence']) else np.nan})
                Amplicon_annotation = pd.Series(Amplicon_annotation)
                Result = Result.assign(Annotation = Amplicon_annotation)
        if output_folder != "":
            if not os.path.exists(output_folder):
                os.mkdir(output_folder)
            Result.to_csv(output_folder+"iPCR_result.csv")
        else:
            if os.path.isfile(input_file):
                if input_file.rfind(".") == -1:
                    Result.to_csv(input_file+"_iPCR_result.csv")
                else:
                    Result.to_csv(input_file[0:input_file.rfind("."):]+"_iPCR_result.csv")
            else:
                if input_file.endswith("/"):
                    Result.to_csv(input_file + "iPCR_result.csv")
                else:
                    Result.to_csv(input_file + "/" + "iPCR_result.csv")
    else:
        trimmed_seqs = []
        if Remain_all_amplicons:
            if np.mean(Seq_no) > len(Seq_no):
                with tqdm(total = np.sum(Seq_no), desc = "Writing PCR result", leave = False, unit = "tasks", unit_scale = True) as pbar:
                    def Progressbar_update_gamma(Result):
                        pbar.update(Result[1])
                    for file_path in file_paths:
                        if Feature:
                            seq_dict = read_sequence_file(input = file_path, format = "genbank", Feature = True)[0]
                            annotation.update({key:seq_dict[key][1] for key in seq_dict})
                            seq_dict = {key:seq_dict[key][0] for key in seq_dict}
                        else:
                            seq_dict = read_sequence_file(file_path)[0]
                        Sequence_length_list = [np.min([amplicon_size_limit, seq_dict[key].sequence_length]) for key in seq_dict]
                        seq_dict = {key:circularDNA(sequence = seq_dict[key], overlap = int(np.min([overlap_region, seq_dict[key].sequence_length]))) if circular_index[key] else circularDNA(sequence = seq_dict[key], overlap = int(0)) for key in seq_dict}
                        if (CPU > 1):
                            with get_context("spawn").Pool(processes = np.min([CPU, len(seq_dict)]), initializer = init_worker) as pl:
                                try:
                                    if Position_index:
                                        trimmed_seq = [(file_path, name, pl.apply_async(PCR_amplicon_with_progress_bar, kwds = {"forward": fwd, "reverse": rev, "template": seq_dict[name], "Single_amplicon": False, "Sequence_Only": False, "amplicon_size_limit": limit, "allowance": allowance, "Warning_ignore": Warning_ignore}, callback = Progressbar_update_gamma), ) for limit, name in zip(Sequence_length_list, seq_dict)]
                                    else:
                                        trimmed_seq = [(file_path, name, pl.apply_async(PCR_amplicon_with_progress_bar, kwds = {"forward": fwd, "reverse": rev, "template": seq_dict[name], "Single_amplicon": False, "Sequence_Only": True, "amplicon_size_limit": limit, "allowance": allowance, "Warning_ignore": Warning_ignore}, callback = Progressbar_update_gamma), ) for limit, name in zip(Sequence_length_list, seq_dict)]
                                except KeyboardInterrupt:
                                    pl.terminate()
                                    pl.join()
                                    pl.close()
                                    print("\n\n --- Keyboard Interrupt ---")
                                    sys.exit("")
                                trimmed_seq = [(ts[0], ts[1], ts[2].get()[0], ) for ts in trimmed_seq]
                        else:
                            if Position_index:
                                trimmed_seq = [(file_path, name, PCR_amplicon(forward = fwd, reverse = rev, template = seq_dict[name], Single_amplicon = False, Sequence_Only = False, amplicon_size_limit = limit, allowance = allowance, Warning_ignore = Warning_ignore), pbar.update(1), ) for limit, name in zip(Sequence_length_list, seq_dict)]
                            else:
                                trimmed_seq = [(file_path, name, PCR_amplicon(forward = fwd, reverse = rev, template = seq_dict[name], Single_amplicon = False, Sequence_Only = True, amplicon_size_limit = limit, allowance = allowance, Warning_ignore = Warning_ignore), pbar.update(1), ) for limit, name in zip(Sequence_length_list, seq_dict)]
                        trimmed_seq = [ts for ts in trimmed_seq if ts[2] is not None]
                        if Position_index & Feature & (len(annotation) > 0): 
                            annotated_trimmed_seq = []
                            for ts in trimmed_seq: 
                                Gene = [[position for position in re.sub(r"[^0-9]+", " ", target).split(" ") if len(position) != 0] + [annotation[ts[1]][target]] for target in annotation[ts[1]].keys() if (ts[1] in annotation.keys())] 
                                Amplicon_annotation = {str(amp[0]) + str(amp[1]): [(g[0], g[1], g[2], ) for g in Gene if (((int(g[0]) - int(distance)) <= np.abs(amp[0])) & ((int(g[1]) + int(distance)) >= np.abs(amp[0]))) | (((int(g[0]) - int(distance)) <= np.abs(amp[1])) & ((int(g[1]) + int(distance)) >= np.abs(amp[1]))) | (((int(g[0]) - int(distance)) >= np.abs(amp[0])) & ((int(g[1]) + int(distance)) <= np.abs(amp[1])))] for amp in ts[2]} 
                                annotated_trimmed_seq.append((ts[0], ts[1], [tuple(list(amp) + [Amplicon_annotation[str(amp[0]) + str(amp[1])]]) for amp in ts[2]], )) 
                            trimmed_seq = ([[(ts[0], ts[1]+"_amplicon_"+str(j+1)+"_("+str(seq[0])+" -> "+str(seq[1])+")", seq[2], seq[3], ) for j, seq in enumerate(ts[2])] if len(ts[2]) > 0 else ts for ts in annotated_trimmed_seq]) if len(annotated_trimmed_seq) > 0 else annotated_trimmed_seq 
                            del annotated_trimmed_seq
                        elif Position_index:
                            trimmed_seq = ([[(ts[0], ts[1]+"_amplicon_"+str(j+1)+"_("+str(seq[0])+" -> "+str(seq[1])+")", seq[2], [], ) for j, seq in enumerate(ts[2])] if len(ts[2]) > 0 else ts for ts in trimmed_seq]) if len(trimmed_seq) > 0 else trimmed_seq
                        else:
                            trimmed_seq = ([[(ts[0], ts[1]+"_amplicon_"+str(j+1), seq, [], ) for j, seq in enumerate(ts[2])] if len(ts[2]) > 0 else ts for ts in trimmed_seq]) if len(trimmed_seq) > 0 else trimmed_seq
                        trimmed_seq = list(it.chain.from_iterable(trimmed_seq))
                        trimmed_seqs += trimmed_seq
            else:
                if Feature: 
                    for file_path in file_paths: 
                        seq_dict = read_sequence_file(input = file_path, format = "genbank", Feature = True)[0] 
                        annotation.update({key:seq_dict[key][1] for key in seq_dict}) 
                        del seq_dict 
                with get_context("spawn").Pool(processes = np.min([CPU, len(file_paths)]), initializer = init_worker) as pl:
                    try:
                        if Position_index & Feature & (len(annotation) > 0):
                            trimmed_seq = list(tqdm(pl.imap(partial(trim_seq_worker_process_all, fwd = fwd, rev = rev, Sequence_Only = False, amplicon_size_limit = amplicon_size_limit, allowance = allowance, Warning_ignore = Warning_ignore, overlap_region = overlap_region, circular_index = circular_index, Feature = Feature, annotation = annotation, distance = distance), file_paths), total = np.sum(Seq_no), desc = "Writing PCR result", leave = False, unit = "tasks", unit_scale = True))
                        elif Position_index:
                            trimmed_seq = list(tqdm(pl.imap(partial(trim_seq_worker_process_all, fwd = fwd, rev = rev, Sequence_Only = False, amplicon_size_limit = amplicon_size_limit, allowance = allowance, Warning_ignore = Warning_ignore, overlap_region = overlap_region, circular_index = circular_index), file_paths), total = np.sum(Seq_no), desc = "Writing PCR result", leave = False, unit = "tasks", unit_scale = True))
                        else:
                            trimmed_seq = list(tqdm(pl.imap(partial(trim_seq_worker_process_all, fwd = fwd, rev = rev, Sequence_Only = True, amplicon_size_limit = amplicon_size_limit, allowance = allowance, Warning_ignore = Warning_ignore, overlap_region = overlap_region, circular_index = circular_index), file_paths), total = np.sum(Seq_no), desc = "Writing PCR result", leave = False, unit = "tasks", unit_scale = True))
                    except KeyboardInterrupt:
                        pl.terminate()
                        pl.join()
                        pl.close()
                        print("\n\n --- Keyboard Interrupt ---")
                        sys.exit("")
                trimmed_seqs = list(it.chain.from_iterable(trimmed_seq))
        else:
            if np.mean(Seq_no) > len(Seq_no):
                with tqdm(total = np.sum(Seq_no), desc = "Writing PCR result", leave = False, unit = "tasks", unit_scale = True) as pbar:
                    def Progressbar_update_delta(Result):
                        pbar.update(Result[1])
                    for file_path in file_paths:
                        if Feature:
                            seq_dict = read_sequence_file(input = file_path, format = "genbank", Feature = True)[0]
                            annotation.update({key:seq_dict[key][1] for key in seq_dict})
                            seq_dict = {key:seq_dict[key][0] for key in seq_dict}
                        else:
                            seq_dict = read_sequence_file(file_path)[0]
                        Sequence_length_list = [np.min([amplicon_size_limit, seq_dict[key].sequence_length]) for key in seq_dict]
                        seq_dict = {key:circularDNA(sequence = seq_dict[key], overlap = int(np.min([overlap_region, seq_dict[key].sequence_length]))) if circular_index[key] else circularDNA(sequence = seq_dict[key], overlap = int(0)) for key in seq_dict}
                        if (CPU > 1):
                            with get_context("spawn").Pool(processes = np.min([CPU, len(seq_dict)]), initializer = init_worker) as pl:
                                try:
                                    if Position_index:
                                        trimmed_seq = [(file_path, name, pl.apply_async(PCR_amplicon_with_progress_bar, kwds = {"forward": fwd, "reverse": rev, "template": seq_dict[name], "Single_amplicon": True, "Sequence_Only": False, "amplicon_size_limit": limit, "allowance": allowance, "Warning_ignore": Warning_ignore}, callback = Progressbar_update_delta), ) for limit, name in zip(Sequence_length_list, seq_dict)]
                                    else:
                                        trimmed_seq = [(file_path, name, pl.apply_async(PCR_amplicon_with_progress_bar, kwds = {"forward": fwd, "reverse": rev, "template": seq_dict[name], "Single_amplicon": True, "Sequence_Only": True, "amplicon_size_limit": limit, "allowance": allowance, "Warning_ignore": Warning_ignore}, callback = Progressbar_update_delta), ) for limit, name in zip(Sequence_length_list, seq_dict)]
                                except KeyboardInterrupt:
                                    pl.terminate()
                                    pl.join()
                                    pl.close()
                                    print("\n\n --- Keyboard Interrupt ---")
                                    sys.exit("")
                                trimmed_seq = [(ts[0], ts[1], ts[2].get()[0], ) for ts in trimmed_seq]
                        else:
                            if Position_index:
                                trimmed_seq = [(file_path, name, PCR_amplicon(forward = fwd, reverse = rev, template = seq_dict[name], Single_amplicon = True, Sequence_Only = False, amplicon_size_limit = limit, allowance = allowance, Warning_ignore = Warning_ignore), pbar.update(1), ) for limit, name in zip(Sequence_length_list, seq_dict)]
                            else:
                                trimmed_seq = [(file_path, name, PCR_amplicon(forward = fwd, reverse = rev, template = seq_dict[name], Single_amplicon = True, Sequence_Only = True, amplicon_size_limit = limit, allowance = allowance, Warning_ignore = Warning_ignore), pbar.update(1), ) for limit, name in zip(Sequence_length_list, seq_dict)]
                        trimmed_seq = [ts for ts in trimmed_seq if ts[2] is not None]
                        if Position_index & Feature & (len(annotation) > 0): 
                            annotated_trimmed_seq = []
                            for ts in trimmed_seq: 
                                Gene = [[position for position in re.sub(r"[^0-9]+", " ", target).split(" ") if len(position) != 0] + [annotation[ts[1]][target]] for target in annotation[ts[1]].keys() if (ts[1] in annotation.keys())] 
                                Amplicon_annotation = {str(ts[2][0]) + str(ts[2][1]): [(g[0], g[1], g[2], ) for g in Gene if (((int(g[0]) - int(distance)) <= np.abs(ts[2][0])) & ((int(g[1]) + int(distance)) >= np.abs(ts[2][0]))) | (((int(g[0]) - int(distance)) <= np.abs(ts[2][1])) & ((int(g[1]) + int(distance)) >= np.abs(ts[2][1]))) | (((int(g[0]) - int(distance)) >= np.abs(ts[2][0])) & ((int(g[1]) + int(distance)) <= np.abs(ts[2][1])))]} 
                                annotated_trimmed_seq.append((ts[0], ts[1], tuple(list(ts[2]) + [Amplicon_annotation[str(ts[2][0]) + str(ts[2][1])]]), )) 
                            trimmed_seq = [(ts[0], ts[1]+"_("+str(ts[2][0])+" -> "+str(ts[2][1])+")", ts[2][2], ts[2][3], ) for ts in annotated_trimmed_seq] 
                            del annotated_trimmed_seq
                        elif Position_index:
                            trimmed_seq = [(ts[0], ts[1]+"_("+str(ts[2][0])+" -> "+str(ts[2][1])+")", ts[2][2], [], ) for ts in trimmed_seq]
                        else:
                            trimmed_seq = [(ts[0], ts[1], ts[2], [], ) for ts in trimmed_seq]
                        trimmed_seqs += trimmed_seq
            else:
                if Feature: 
                    for file_path in file_paths: 
                        seq_dict = read_sequence_file(input = file_path, format = "genbank", Feature = True)[0] 
                        annotation.update({key:seq_dict[key][1] for key in seq_dict}) 
                        del seq_dict 
                with get_context("spawn").Pool(processes = np.min([CPU, len(file_paths)]), initializer = init_worker) as pl:
                    try:
                        if Position_index & Feature & (len(annotation) > 0):
                            trimmed_seqs = list(tqdm(pl.imap(partial(trim_seq_worker_process_single, fwd = fwd, rev = rev, Sequence_Only = False, amplicon_size_limit = amplicon_size_limit, allowance = allowance, Warning_ignore = Warning_ignore, overlap_region = overlap_region, circular_index = circular_index, Feature = Feature, annotation = annotation, distance = distance), file_paths), total = np.sum(Seq_no), desc = "Writing PCR result", leave = False, unit = "tasks", unit_scale = True))
                        elif Position_index:
                            trimmed_seqs = list(tqdm(pl.imap(partial(trim_seq_worker_process_single, fwd = fwd, rev = rev, Sequence_Only = False, amplicon_size_limit = amplicon_size_limit, allowance = allowance, Warning_ignore = Warning_ignore, overlap_region = overlap_region, circular_index = circular_index), file_paths), total = np.sum(Seq_no), desc = "Writing PCR result", leave = False, unit = "tasks", unit_scale = True))
                        else:
                            trimmed_seqs = list(tqdm(pl.imap(partial(trim_seq_worker_process_single, fwd = fwd, rev = rev, Sequence_Only = True, amplicon_size_limit = amplicon_size_limit, allowance = allowance, Warning_ignore = Warning_ignore, overlap_region = overlap_region, circular_index = circular_index), file_paths), total = np.sum(Seq_no), desc = "Writing PCR result", leave = False, unit = "tasks", unit_scale = True))
                    except KeyboardInterrupt:
                        pl.terminate()
                        pl.join()
                        pl.close()
                        print("\n\n --- Keyboard Interrupt ---")
                        sys.exit("")
                trimmed_seqs = list(it.chain.from_iterable(trimmed_seqs))
        if len(trimmed_seqs) == 0:
            print("No amplicon was obtained.")
            sys.exit()
        if output_folder != "":
            if not os.path.exists(output_folder):
                os.mkdir(output_folder)
            if single_file:
                for trimmed_seq in trimmed_seqs:
                    with open(output_folder+"iPCR_result.fasta", "a", encoding = "utf-8") as fout:
                        fout.write(">"+trimmed_seq[1]+"\n"+trimmed_seq[2]+"\n")
            elif Feature:
                for trimmed_seq in trimmed_seqs:
                    with open(output_folder + re.sub(r'_(.)_', r'\1', re.sub(r' (.) ', r'\1', re.sub(r'\.|,|-|>', "", str(trimmed_seq[1])))).replace("  ", " ").replace(" ", "_") + ".gb", "wt", encoding = "utf-8") as fout:
                        seq =  str(trimmed_seq[2])
                        Gene = trimmed_seq[3]
                        split_sequence_list = [seq[i * 10:(i+1) * 10:] for i in range(len(seq) // 10 + 1)]
                        Sequence = "".join([" ".join([str(i * 60 + 1).rjust(9)] + split_sequence_list[i * 6 : (i + 1) * 6:] + ["\n"]) for i in range(sum([len(split_sequence) == 10 for split_sequence in split_sequence_list]) // 6 + 1)])
                        LOCUS = "LOCUS".ljust(12) + str(trimmed_seq[1])
                        DEFINITION = "DEFINITION".ljust(12) + str(trimmed_seq[1])
                        TITLE = "TITLE".ljust(12) + str(trimmed_seq[1])
                        FEATURES = "FEATURES             Location/Qualifiers"
                        annotation_template1 = "     CDS             {0}..{1}" + "\n" + "".ljust(21) + '/product="{2}"'
                        annotation_template2 = "     CDS             complement({1}..{0})" + "\n" + "".ljust(21) + '/product="{2}"'
                        ANNOTATION = "\n".join([annotation_template1.format(g[0], g[1], g[2]) if int(g[0]) > 0 else annotation_template2.format(g[0], g[1], g[2]) for g in Gene])
                        SEQUENCE = "ORIGIN\n\n" + Sequence + "//"
                        OUTPUT_DATA = LOCUS + "\n" + DEFINITION + "\n" + TITLE + "\n" + FEATURES + "\n" + ANNOTATION + "\n" + SEQUENCE
                        fout.write(OUTPUT_DATA)
            else:
                for trimmed_seq in trimmed_seqs:
                    with open(output_folder+trimmed_seq[0][trimmed_seq[0].rfind("/") + 1:].replace(trimmed_seq[0][trimmed_seq[0].rfind("."):], "") + "_iPCR_result.fasta", "a", encoding = "utf-8") as fout:
                        fout.write(">"+trimmed_seq[1]+"\n"+trimmed_seq[2]+"\n")
        else:
            if single_file:
                for trimmed_seq in trimmed_seqs:
                    with open(trimmed_seq[0].replace(trimmed_seq[0][trimmed_seq[0].rfind("/") + 1:], "") + "iPCR_result.fasta", "a", encoding = "utf-8") as fout:
                        fout.write(">"+trimmed_seq[1]+"\n"+trimmed_seq[2]+"\n")
            elif Feature:
                for trimmed_seq in trimmed_seqs:
                    with open(trimmed_seq[0].replace(trimmed_seq[0][trimmed_seq[0].rfind("/") + 1:], "") + re.sub(r'_(.)_', r'\1', re.sub(r' (.) ', r'\1', re.sub(r'\.|,|-|>', "", str(trimmed_seq[1])))).replace("  ", " ").replace(" ", "_") + ".gb", "wt", encoding = "utf-8") as fout:
                        seq =  str(trimmed_seq[2])
                        Gene = trimmed_seq[3]
                        split_sequence_list = [seq[i * 10:(i+1) * 10:] for i in range(len(seq) // 10 + 1)]
                        Sequence = "".join([" ".join([str(i * 60 + 1).rjust(9)] + split_sequence_list[i * 6 : (i + 1) * 6:] + ["\n"]) for i in range(sum([len(split_sequence) == 10 for split_sequence in split_sequence_list]) // 6 + 1)])
                        LOCUS = "LOCUS".ljust(12) + str(trimmed_seq[1])
                        DEFINITION = "DEFINITION".ljust(12) + str(trimmed_seq[1])
                        TITLE = "TITLE".ljust(12) + str(trimmed_seq[1])
                        FEATURES = "FEATURES             Location/Qualifiers"
                        annotation_template1 = "     CDS             {0}..{1}" + "\n" + "".ljust(21) + '/product="{2}"'
                        annotation_template2 = "     CDS             complement({1}..{0})" + "\n" + "".ljust(21) + '/product="{2}"'
                        ANNOTATION = "\n".join([annotation_template1.format(g[0], g[1], g[2]) if int(g[0]) > 0 else annotation_template2.format(g[0], g[1], g[2]) for g in Gene])
                        SEQUENCE = "ORIGIN\n\n" + Sequence + "//"
                        OUTPUT_DATA = LOCUS + "\n" + DEFINITION + "\n" + TITLE + "\n" + FEATURES + "\n" + ANNOTATION + "\n" + SEQUENCE
                        fout.write(OUTPUT_DATA)
            else:
                for trimmed_seq in trimmed_seqs:
                    with open(trimmed_seq[0].replace(trimmed_seq[0][trimmed_seq[0].rfind("."):], "") + "_iPCR_result.fasta", "a", encoding = "utf-8") as fout:
                        fout.write(">"+trimmed_seq[1]+"\n"+trimmed_seq[2]+"\n")