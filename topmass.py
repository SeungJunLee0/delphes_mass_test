import uproot
import awkward as ak
import glob
from multiprocessing import Pool, cpu_count
import os
from tqdm.contrib.concurrent import process_map  # 👈 요거만 추가
import sys

widths = [
    "0_80emu",
    "0_90emu",
    "1_00emu",
    "1_10emu",
    "1_20emu",
    "1_30emu",
    "1_32emu",
    "1_40emu",
    "1_50emu",
    "1_60emu",
    "1_70emu",
    "1_80emu",
]

def select_width(k):
    nu = k#int(k)
    top_mass_output = []
    
    paths = glob.glob("/data1/powheg/"+widths[nu]+"/root/*.root")
    #paths = glob.glob("/data1/powheg/0_80emu/root/*.root")
    exclude_files = {
        "ttbar_powheg_pythia_CP5_delphes_1_80emu_0056.root",
        "ttbar_powheg_pythia_CP5_delphes_1_80emu_0099.root",
        "ttbar_powheg_pythia_CP5_delphes_1_80emu_0159.root",
        "ttbar_powheg_pythia_CP5_delphes_1_40emu_0051.root",
        "ttbar_powheg_pythia_CP5_delphes_1_20emu_0116.root",
        "ttbar_powheg_pythia_CP5_delphes_1_10emu_0132.root",
        "ttbar_powheg_pythia_CP5_delphes_1_10emu_0138.root",
        "ttbar_powheg_pythia_CP5_delphes_1_10emu_0157.root",
        "ttbar_powheg_pythia_CP5_delphes_1_10emu_0159.root",
        "ttbar_powheg_pythia_CP5_delphes_1_10emu_0148.root", 
        "ttbar_powheg_pythia_CP5_delphes_1_00emu_0065.root",
        "ttbar_powheg_pythia_CP5_delphes_0_80emu_0043.root",
        "ttbar_powheg_pythia_CP5_delphes_0_80emu_0013.root",
        "ttbar_powheg_pythia_CP5_delphes_0_80emu_0049.root",
        "ttbar_powheg_pythia_CP5_delphes_0_80emu_0039.root",
        "ttbar_powheg_pythia_CP5_delphes_0_80emu_0056.root",
    }
    all_paths = glob.glob("/data1/powheg/"+widths[nu]+"/root/*.root")
    #all_paths = glob.glob("/data1/powheg/0_80emu/root/*.root")
    file_list = [f for f in all_paths if os.path.basename(f) not in exclude_files]
    return file_list

# 병렬 처리할 함수 정의
def process_file(file_path):
    result = []
    try:
        with uproot.open(file_path) as file:
            tree = file["Delphes"]
            pid_array = tree["Particle.PID"].array()
            mass_array = tree["Particle.Mass"].array()
            status_array = tree["Particle.Status"].array()

            for pid_evt, mass_evt, status_evt in zip(pid_array, mass_array, status_array):
                top_mask = (abs(pid_evt) == 6)
                top_islast = (status_evt == 62)
                top_final_mask = top_mask & top_islast
                top_masses = mass_evt[top_final_mask]
                result.extend(top_masses.tolist())
    except Exception as e:
        print(f"⚠️ 오류 발생: {file_path} → {e}")
    return result

# 멀티프로세싱 Pool 실행
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python topmass.py <index>")
        sys.exit(1)
    nu = int(sys.argv[1])
    #nu = sys.argv
    print(widths[nu])
    
    file_list = select_width(nu)
    # process_map으로 병렬 + tqdm
    results = process_map(
        process_file,
        file_list,
        max_workers=48,     # 사용하고 싶은 코어 수
        chunksize=1         # 파일 1개 단위 처리
    )

    # 결과 합치기
    top_mass_output = [mass for sublist in results for mass in sublist]

    # 저장
    with open("top_mass_list_"+widths[nu]+".txt", "w") as f:
        for mass in top_mass_output:
            f.write(f"{mass}\n")
