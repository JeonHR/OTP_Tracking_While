import logging
import psutil
import subprocess
import time

def normalize_path(path):
    return path.replace('/', '\\')

def is_program_running_at_path(program_path):
    normalized_program_path = normalize_path(program_path)
    for proc in psutil.process_iter(['name', 'exe']):
        if proc.info['exe'] == normalized_program_path:
            return True
    return False

def check_txt_file(file_path, target_line):
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if line_number == target_line and "<LotID>" in line and ".00</LotID>" in line:
                return line
    return None

def run_program(program_path):
    subprocess.Popen(program_path, shell=True)
    print("프로그램을 실행했습니다.")
    logging.info(f"프로그램을 실행했습니다: {program_path}")

def is_program_running(program_name):
    for proc in psutil.process_iter(['name']):
        if program_name.lower() in proc.info['name'].lower():
            return True
    return False

if __name__ == "__main__":
    logging.basicConfig(filename='C:/Users/eagle/Desktop/log_file/log_all.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    program_to_run = "C:/ENG/20240403_Write3_Bin_Sort_1.2.1/OTP_Write3_Bin_Sort_1.2.1.exe"  # 실행할 프로그램 경로
    program_to_run_path = "C:/LitePoint/Tanami/uwbOI.exe"  # 실행할 프로그램의 경로
    program_to_check = "OTP_Write3_Bin_Sort_1.2.1.exe"  # 체크할 프로그램 이름
    txt_file_path = "C:/LitePoint/Tanami/lotSetup.xml"  # 특정 txt 파일 경로
    target_line = 4  # 확인할 특정 라인 번호

    while True:
        # 프로그램 실행 상태 확인
        if is_program_running_at_path(program_to_run_path):
            print(f"{program_to_run_path} 프로그램이 실행 중입니다. 종료를 대기합니다.")
            
            # 내부 루프: 프로그램 종료 상태 확인
            while is_program_running_at_path(program_to_run_path):
                time.sleep(10)
            
            print(f"{program_to_run_path} 프로그램이 종료되었습니다. 조건을 확인합니다.")
            logging.info(f"{program_to_run_path} 프로그램이 종료되었습니다. 조건을 확인합니다.")

            # 프로그램 종료 후 조건 확인
            if not is_program_running(program_to_check):
                line = check_txt_file(txt_file_path, target_line)
                if line:
                    print(f"파일에서 조건을 만족하는 라인을 찾았습니다: {line}")
                    logging.info(f"파일에서 조건을 만족하는 라인을 찾았습니다: {line}")
                    run_program(program_to_run)
                else:
                    print(f"파일에서 조건을 만족하는 라인을 찾을 수 없습니다.")
                    logging.info(f"파일에서 조건을 만족하는 라인을 찾을 수 없습니다.")
        
        print("외부 루프를 다시 시작합니다.")
        time.sleep(10)
