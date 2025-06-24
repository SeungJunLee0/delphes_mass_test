import uproot
import awkward as ak
import glob

# 1. 파일 경로 설정
file_list = glob.glob("/data1/powheg/1_32emu/root/ttbar_powheg_pythia_CP5_delphes_1_32emu_0002.root")

# 2. 각 루트 파일에 대해 루프
for file_path in file_list:
    print(f"\n📁 파일: {file_path}")
    with uproot.open(file_path) as file:
        tree = file["Delphes"]

        # 3. PID, Mass 정보 추출
        pid_array = tree["Particle.PID"].array()
        mass_array = tree["Particle.Mass"].array()
        status_array = tree["Particle.Status"].array()

        # 4. 이벤트 루프
        for ievt, (pid_evt, mass_evt) in enumerate(zip(pid_array, mass_array)):
            # PID가 ±6인 (top quark) 입자 선택
            top_mask = (abs(pid_evt) == 6)
            top_masses = mass_evt[top_mask]
            top_status = status_array[top_mask]

            # top quark가 있다면 출력
            if len(top_masses) > 0:
                print(f"이벤트 {ievt}: top quark mass =", top_masses.tolist())
                print(f"이벤트 {ievt}: top quark mass =", top_status.tolist())
            if ievt >=10:
                break
