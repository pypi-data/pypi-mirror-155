import sys
import os
import shutil
import re
import glob
import math
import filecmp
import pandas as pd
from multiprocessing import cpu_count
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from shrs import AdditionalAnalysis, DesignIdentifyPrimer, DesignUniversalPrimer, InputSequencePreprocessing, insilicoPCR

#shrs AA -i AdditionalAnalysis_sample.fasta -f AdditionalAnalysis_template.csv
def test_AdditionalAnalysis():
    Ref1 = pd.read_csv("./tests/AA_reference1.csv", header = 0)
    Ref2 = pd.read_csv("./tests/AA_reference2.csv", header = None, names = range(13))
    class args():
        def __init__(self, no):
            self.input_file = "./tests/AdditionalAnalysis_sample1.fasta" if no == 1 else "./tests/AdditionalAnalysis_sample2.fasta"
            self.csv_file = "./tests/AdditionalAnalysis_template1.csv" if no == 1 else "./tests/AdditionalAnalysis_template2.csv"
            self.output = "./tests/"
            self.size_limit = int(10000)
            self.process = math.ceil(cpu_count() / 2)
            self.forward = None 
            self.reverse = None
            self.circularDNA = None
            self.warning = True
    Test_ = args(1)
    AdditionalAnalysis.AdditionalAnalysis(Test_)
    Test_ = args(2)
    AdditionalAnalysis.AdditionalAnalysis(Test_)
    Result_path1 = glob.glob("./tests/**/*template1_Additional_Analysis_result.csv", recursive = True)
    Result_path2 = glob.glob("./tests/**/*template2_Additional_Analysis_result.csv", recursive = True)
    Test1 = pd.read_csv(Result_path1[0], header = 0)
    Test2 = pd.read_csv(Result_path2[0], header = None, names = range(13))
    Result1 = (Test1.fillna(0) == Ref1.fillna(0)).all().all()
    Result2 = (Test2.fillna(0) == Ref2.fillna(0)).all().all()
    Result = Result1 & Result2
    del Test1, Test2, Result1, Result2
    os.remove(Result_path1[0])
    os.remove(Result_path2[0])
    assert Result

#shrs ISP -i ISP_sample.fasta
def test_InputSequencePreprocessing():
    class args():
        def __init__(self):
            self.input_file = "./tests/ISP_sample.fasta"
            self.output = "./tests/"
            self.circularDNA = None
            self.circularDNAoverlap = int(10000)
            self.Single_target = True
            self.Multiple_targets = False
            self.Single_file = False
    Test_ = args()
    InputSequencePreprocessing.InputSequencePreprocessing(Test_)
    Result_path = glob.glob("./tests/**/Preprocessed_ISP_sample.fasta", recursive = True)
    Result = filecmp.cmp("./tests/ISP_reference.fasta", Result_path[0])
    os.remove(Result_path[0])
    assert Result

#shrs iPCR -i insilicoPCR_sample.gb -fwd AATGATGTTAATRATKYTGAAGWTA -rev AAATTTACATCCTCAACCAAGGTTT -c --Annotation --Remain_all_amplicons
def test_insilicoPCR():
    Ref = pd.read_csv("./tests/iPCR_reference.csv")
    class args():
        def __init__(self):
            self.input_file = "./tests/iPCR_sample.gb"
            self.output = "./tests/"
            self.size_limit = int(10000)
            self.process = math.ceil(cpu_count() / 2)
            self.fasta = True
            self.forward = "AATGATGTTAATRATKYTGAAGWTA"
            self.reverse = "AAATTTACATCCTCAACCAAGGTTT"
            self.Single_file = False
            self.Mismatch_allowance = int(0)
            self.Only_one_amplicon = True
            self.Position_index = False
            self.circularDNA = None
            self.gene_annotation_search_range = int(100)
            self.Annotation = True
            self.warning = True
    Test_ = args()
    insilicoPCR.insilicoPCR(Test_)
    Result_path = glob.glob("./tests/**/*iPCR_result.csv", recursive = True)
    Test = pd.read_csv(Result_path[0])
    Result = (Test.fillna(0) == Ref.fillna(0)).all().all()
    os.remove(Result_path[0])
    assert Result

#shrs DIP -i Test_samples.fasta -e Test_removal.fasta --Search_mode sparse
def test_DesignIdentifyPrimer():
    Ref = pd.read_csv("./tests/DIP_reference.csv", sep = ",", names = range(10))
    class args():
        def __init__(self):
            self.input_file = "./tests/samples_sequences.fasta"
            self.exclude_file = "./tests/removal_sequence.fasta"
            self.primer_size = int(25)
            self.allowance = float(0.15)
            self.range = int(0)
            self.distance = int(10000)
            self.output = "./tests/"
            self.process = math.ceil(cpu_count() / 2)
            self.Exclude_mode = "fast"
            self.Result_output = int(10000)
            self.Cut_off_lower = float(50)
            self.Cut_off_upper = float(1000)
            self.Match_rate = float(0.8)
            self.Chunks = "Auto"
            self.Maximum_annealing_site_number = int(5)
            self.Window_size = int(950)
            self.Search_mode = ["sparse"]
            self.withinMemory = True
            self.Without_allowance_adjustment = True
            self.circularDNA = None
            self.exclude_circularDNA = None
            self.Score_calculation = 'Fragment'
            self.Fragment_size_pattern_matrix = None
            self.Fragment_start_position_matrix = None
    Test_ = args()
    DesignIdentifyPrimer.DesignIdentifyPrimer(Test_)
    Result_path = glob.glob("./tests/Result/**identify_primer_set/*Summary.csv", recursive = True)
    Test = pd.read_csv(Result_path[0], sep = ",", names = range(10))
    Test_row = Test.shape[0]
    Ref_row = Ref.shape[0]
    MIN_ROW = min([Test_row, Ref_row])
    Result = (Test.fillna(0).iloc[16:MIN_ROW] == Ref.fillna(0).iloc[16:MIN_ROW]).all().all()
    shutil.rmtree("./tests/Result/")
    assert Result

#shrs DUP -i Test_samples.fasta -e Test_removal.fasta --Search_mode sparse
def test_DesignUniversdalPrimer():
    Ref = pd.read_csv("./tests/DUP_reference.csv", sep = ",", names = range(10))
    class args():
        def __init__(self):
            self.input_file = "./tests/samples_sequences.fasta"
            self.exclude_file = "./tests/removal_sequence.fasta"
            self.primer_size = int(20)
            self.allowance = float(0.25)
            self.range = int(0)
            self.distance = int(100)
            self.output = "./tests/"
            self.process = math.ceil(cpu_count() / 2)
            self.Exclude_mode = "fast"
            self.Result_output = int(10000)
            self.Cut_off_lower = float(50)
            self.Cut_off_upper = float(10000)
            self.Match_rate = float(0.0)
            self.Chunks = "Auto"
            self.Maximum_annealing_site_number = None
            self.Window_size = int(50)
            self.Omit_similar_fragment_size_pair = False
            self.Search_mode = ["sparse"]
            self.withinMemory = True
            self.Without_allowance_adjustment = True
            self.circularDNA = None
            self.exclude_circularDNA = None
            self.Fragment_size_pattern_matrix = None
    Test_ = args()
    DesignUniversalPrimer.DesignUniversalPrimer(Test_)
    Result_path = glob.glob("./tests/Result/**universal_primer_set/*Summary.csv", recursive = True)
    Test = pd.read_csv(Result_path[0], sep = ",", names = range(10))
    Test_row = Test.shape[0]
    Ref_row = Ref.shape[0]
    MIN_ROW = min([Test_row, Ref_row])
    Result = (Test.fillna(0).iloc[14:MIN_ROW] == Ref.fillna(0).iloc[14:MIN_ROW]).all().all()
    shutil.rmtree("./tests/Result/")
    assert Result