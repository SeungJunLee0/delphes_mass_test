import uproot
import awkward as ak
import glob

top_mass_output = []

paths = glob.glob("/data1/powheg/0_80emu/root/*.root")
exclude_files = {
    "ttbar_powheg_pythia_CP5_delphes_0_80emu_0043.root",
    "ttbar_powheg_pythia_CP5_delphes_0_80emu_0013.root",
    "ttbar_powheg_pythia_CP5_delphes_0_80emu_0049.root",
    "ttbar_powheg_pythia_CP5_delphes_0_80emu_0039.root",
    "ttbar_powheg_pythia_CP5_delphes_0_80emu_0056.root",
}
all_paths = glob.glob("/data1/powheg/0_80emu/root/*.root")
file_list = [f for f in all_paths if os.path.basename(f) not in exclude_files]

for file_path in file_list:
    print(f"\n📁 파일: {file_path}")
    with uproot.open(file_path) as file:
        tree = file["Delphes"]
        pid_array = tree["Particle.PID"].array()
        mass_array = tree["Particle.Mass"].array()
        status_array = tree["Particle.Status"].array()

        for ievt, (pid_evt, mass_evt, status_evt) in enumerate(zip(pid_array, mass_array, status_array)):
            top_mask = (abs(pid_evt) == 6)
            top_islast = (status_evt == 62)
            top_final_mask = top_mask & top_islast
            top_masses = mass_evt[top_final_mask]

            # 추출
            top_mass_output.extend(top_masses.tolist())


# 저장
with open("top_mass_list.txt", "w") as f:
    for mass in top_mass_output:
        f.write(f"{mass}\n")

