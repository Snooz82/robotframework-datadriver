from robot.run import run

# robot -d logs --listener RobotStackTracer --exclude performanceORfailingORfiltered --loglevel TRACE:INFO --extension robot .

result = run(
    ".",
    outputdir="logs",
    listener="RobotStackTracer",
    exclude="performanceORfailingORfiltered",
    loglevel="TRACE:INFO",
    extension="robot",
)
print(result)
