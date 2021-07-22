import pathlib

from robot import run_cli

project_root = pathlib.Path(__file__).parent.resolve()

def main():
    run_cli(
        [
            f"--argumentfile={project_root}/atest/rf_cli.args",
            f"--variable=root:{project_root}",
            f"{project_root}/atest/TestCases",
        ]
    )

if __name__ == "__main__":
    main()
