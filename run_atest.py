import pathlib
import subprocess

project_root = pathlib.Path(__file__).parent.resolve()

def main():
    cmd =[
        "coverage",
        "run",
        "-m",
        "robot",
        f"--argumentfile={project_root}/atest/rf_cli.args",
        f"--variable=root:{project_root}",
        f"--outputdir={project_root}/atest/logs",
        f"{project_root}/atest/TestCases",
    ]
    subprocess.run(cmd)
    subprocess.run(["coverage", "report"])
    subprocess.run(["coverage", "html"])


if __name__ == "__main__":
    main()
