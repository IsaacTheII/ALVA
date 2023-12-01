import subprocess

def execute_script(script_path, conda_env, video_path):
    command = f"conda run -n {conda_env} python {script_path} {video_path}"
    subprocess.run(command, shell=True)

# Execute script with ALVA conda environment
#execute_script("/path/to/alva_script.py", "ALVA")

# Execute script with PIFPAF conda environment
#execute_script("/path/to/pifpaf_script.py", "PIFPAF")
