import scipy.sparse as sp
import os
import time
import re
import sys
import logging
import csv
import numpy as np

def sum_values(path, start_col, isFirst=False):
    sparse_matrix = (sp.load_npz(path)).tocsr()
    if isFirst: start_col = 0  
    sparse_matrix_subset = sparse_matrix[:, start_col:]
    return sparse_matrix_subset.sum()

def get_heat_map_number(filename):
     nums = re.findall(r'\d+', filename)
     return int(nums[-1])   # last integer in the filename



csv_path = "hitrate_real_summary.csv"

def write_result(trace_name, hit_rate):
    header = ["trace", "hit_rate"]
    exists = os.path.exists(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(header)
        writer.writerow([trace_name, hit_rate])


def compute_accuracy(full_trace, miss_trace, start_col, flag): #computes accuracy of a single program trace
    
    full_filenames = sorted(os.listdir(full_trace), key=get_heat_map_number)
    miss_filenames = sorted(os.listdir(miss_trace), key=get_heat_map_number)
    # assert len(full_filenames) == len(miss_filenames)
    # file_size = len(full_filenames) if len(full_filenames) > len(miss_filenames) else len(miss_filenames)
    file_size = 1000
    accesses, generated_count, misses = 0, 0, 0

    start_time = time.time()
    
    for i in range(file_size):
        isFirst = True if i==0 else False
  
        try: 
            full_file_path = os.path.join(full_trace, full_filenames[i])
            if os.path.isfile(full_file_path):
                # print(sum_values(full_file_path, start_col, isFirst))
                accesses += sum_values(full_file_path, start_col, isFirst)
        except:
            continue

        try:
            miss_file_path = os.path.join(miss_trace, miss_filenames[i])

            if os.path.isfile(miss_file_path):
                # print(sum_values(sum_values(miss_file_path, start_col, isFirst)))
                generated_count += sum_values(miss_file_path, start_col, isFirst)
        except:
            continue

    trace_name = os.path.basename(full_trace)

    # print("Trace:%s, TotalAccesses:%.4f, Misses:%.4f" %(trace_name, accesses, generated_count))
    hit_rate = 0.0
    print(f"[DEBUG] trace={os.path.basename(full_trace)} "
        f"accesses={accesses}, generated_count={generated_count}")
    if generated_count!=0 and generated_count<=accesses:
        if flag == "missmap":
            misses = generated_count
            print(generated_count)
            hit_rate = 1.0 - (generated_count / accesses)
        elif flag == "hitmap":
            misses = accesses - generated_count
            hit_rate = (generated_count / accesses)
    end_time = time.time()

    print(hit_rate, accesses, misses)
    print("Trace:%s, HitRate:%.10f, TotalAccesses:%.4f, Misses:%.4f, CalcTime:%.4f" %(trace_name, hit_rate, accesses, misses, (end_time-start_time)))
    logging.info("Trace:%s, HitRate:%.10f, TotalAccesses:%.4f, Misses:%.4f, CalcTime:%.4f" %(trace_name, hit_rate, accesses, misses, (end_time-start_time)))
    write_result(trace_name, hit_rate)

    return 


def compute_accuracies(full_directory, miss_directory, sparse_mat_shape, flag):
    # full_traces = os.listdir(full_directory)
    miss_traces = os.listdir(miss_directory)
    start_col = int(0.3 * sparse_mat_shape) + 1
    notlst = []
    # if flag == "custom":
    # #    trace_lst = ['602.gcc_s-2375B', '465.tonto-44B', '602.gcc_s-2226B', '445.gobmk-30B', '621.wrf_s-8100B', '631.deepsjeng_s-928B', '607.cactuBSSN_s-4248B', '627.cam4_s-490B', '607.cactuBSSN_s-2421B', '403.gcc-16B', '445.gobmk-36B', '638.imagick_s-824B', '638.imagick_s-10316B', '470.lbm-1274B', '657.xz_s-4994B', '621.wrf_s-575B', '450.soplex-92B', '600.perlbench_s-570B', '403.gcc-48B', '450.soplex-247B', '621.wrf_s-6673B', '465.tonto-1914B', '602.gcc_s-734B', '400.perlbench-41B', '403.gcc-17B', '657.xz_s-56B', '607.cactuBSSN_s-4004B', '607.cactuBSSN_s-3477B', '657.xz_s-2302B', '600.perlbench_s-1273B', '627.cam4_s-573B', '638.imagick_s-4128B', '445.gobmk-2B', '400.perlbench-50B', '445.gobmk-17B', '657.xz_s-3167B', '602.gcc_s-1850B', '600.perlbench_s-210B', '621.wrf_s-8065B']
    #     trace_lst = []
    # elif flag == 'all':
    trace_lst = miss_traces
    # if flag == "notlst":
        # notlst = ['625.x264_s-18B', '459.GemsFDTD-1320B', '623.xalancbmk_s-202B', '458.sjeng-283B', '602.gcc_s-1850B', '456.hmmer-191B', '483.xalancbmk-127B', '483.xalancbmk-736B', '648.exchange2_s-1511B', '619.lbm_s-2676B', '654.roms_s-1070B', '628.pop2_s-17B', '648.exchange2_s-1247B', '454.calculix-460B', '429.mcf-217B', '600.perlbench_s-570B', '462.libquantum-714B', '481.wrf-1170B', '605.mcf_s-782B', '627.cam4_s-490B', '437.leslie3d-232B', '454.calculix-104B', '437.leslie3d-273B', '481.wrf-1254B', '400.perlbench-41B', '654.roms_s-842B', '401.bzip2-7B', '600.perlbench_s-210B', '464.h264ref-57B', '459.GemsFDTD-765B', '410.bwaves-1963B', '429.mcf-51B', '444.namd-426B', '623.xalancbmk_s-10B', '429.mcf-22B', '444.namd-120B', '648.exchange2_s-387B', '644.nab_s-12521B', '459.GemsFDTD-1211B', '641.leela_s-149B', '623.xalancbmk_s-325B', '453.povray-576B', '471.omnetpp-188B', '621.wrf_s-6673B', '621.wrf_s-8100B', '605.mcf_s-1644B', '433.milc-127B', '603.bwaves_s-2931B', '410.bwaves-2097B', '434.zeusmp-10B', '648.exchange2_s-1699B', '437.leslie3d-134B', '473.astar-42B', '401.bzip2-38B', '435.gromacs-111B', '657.xz_s-4994B', '456.hmmer-88B', '481.wrf-1281B', '445.gobmk-30B', '403.gcc-48B', '482.sphinx3-1297B', '483.xalancbmk-716B', '619.lbm_s-4268B', '465.tonto-1914B', '649.fotonik3d_s-10881B', '482.sphinx3-1100B', '481.wrf-816B', '654.roms_s-1390B', '464.h264ref-97B', '620.omnetpp_s-874B', '437.leslie3d-271B', '654.roms_s-1613B', '657.xz_s-2302B']

    for j in range(len(trace_lst)):
        # if trace_lst[j] != '638.imagick_s-4128B':
        if trace_lst[j] in notlst:
            continue
        full_trace = os.path.join(full_directory, trace_lst[j])
        miss_trace = os.path.join(miss_directory, trace_lst[j])

        print("starting ", full_trace)
        compute_accuracy(full_trace, miss_trace, start_col, flag)
        # print("returns here")

        


if __name__ == "__main__":
    assert sys.argv[1] and sys.argv[2] and sys.argv[3] and sys.argv[4] and sys.argv[5]

    full_directory = sys.argv[1]
    miss_directory = sys.argv[2]
    sparse_mat_shape = int(sys.argv[3])
    logfile = sys.argv[4]
    flag = sys.argv[5]

    logging.basicConfig(level=logging.DEBUG, filename=logfile, filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    compute_accuracies(full_directory, miss_directory, sparse_mat_shape, flag)



    ## For no overlap, just set isFirst in line 41 to False