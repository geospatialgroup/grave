import subprocess

# 定义要执行的 Python 脚本文件列表
scripts = [
    "detect.py",  # 第一个 Python 文件
    "detect2.py",# 第二个 Python 文件
    "detect3.py",
]

# 遍历脚本列表，按顺序执行
for script in scripts:
    try:
        # 调用subprocess.run()来执行Python脚本
        print(f"Executing: {script}")
        subprocess.run(["python", script], check=True)  # 使用python3来运行脚本
        print(f"{script} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing {script}: {e}")
        break  # 如果某个脚本执行失败，终止后续执行
