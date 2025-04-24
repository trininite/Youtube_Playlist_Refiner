import subprocess

#.mirror_creation_test_info.txt contents:
#1
#URL
#PATH
with open("./tests/.mirror_creation_test_info.txt", "r") as f:
    input_data = f.read()



result = subprocess.run(
    ['python3', 'src/main.py'],
    input=input_data,
    text=True,  # handles str instead of bytes
    capture_output=True  # gets stdout/stderr
)

print("stdout:", result.stdout)
print("stderr:", result.stderr)
print("exit code:", result.returncode)
