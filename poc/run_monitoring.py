import datetime
import subprocess


def report_level():
	cmd_exec = subprocess.run(
		"bash /home/pi/monitor_audio.sh",
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		shell = True
	)

	recorded_db = cmd_exec.stdout.decode("utf-8").strip()
	current_timestamp = str(datetime.datetime.now())

	return "{}|{}".format(current_timestamp, recorded_db)


def main():
    for run_report in range(20):
        print(report_level())


if __name__ == "__main__":
	main()