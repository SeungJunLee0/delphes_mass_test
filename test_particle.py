import uproot
import glob

# 아무 Delphes 루트 파일 하나만 사용
file_list = glob.glob("/data1/powheg/1_32emu/root/ttbar_powheg_pythia_CP5_delphes_1_32emu_0002.root")
if not file_list:
    raise RuntimeError("ROOT 파일을 찾을 수 없습니다!")

file_path = file_list[0]
print(f"📁 사용 중인 파일: {file_path}")

with uproot.open(file_path) as file:
    tree = file["Delphes"]
    
    print("\n📋 'Particle.'로 시작하는 브랜치 목록:")
    for key in tree.keys():
        if key.startswith("Particle"):
            print("  -", key)
