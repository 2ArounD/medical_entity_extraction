import os
import signal
import subprocess

# # Change directory to where your Flask's app.py is present
os.chdir("./demo")
tf_ic_server = ""
flask_server = ""

try:
    # A Tensorflow SavedModel is served here, from a directory which
    # can contain multiple version of the model
    # versions are placed in folders named with a version number (e.g. 1)
    # This model is being serverd for drugs and chemicals
    tf_ic_server1 = subprocess.Popen(["tensorflow_model_server "
                                      "--model_base_path=" + os.getcwd() + "/../data/SavedModels/BC4CHEMD "
                                      "--port=8500 "
                                      "--rest_api_port=8501 "
                                      "--model_name=BioBert "],
                                     stdout=subprocess.DEVNULL,
                                     shell=True,
                                     preexec_fn=os.setsid)
    print("Tensorflow BioBert-drugs is starting")

    # Another Tensorflow SavedModel is served here
    # This model is being serverd for diseases
    tf_ic_server2 = subprocess.Popen(["tensorflow_model_server "
                                      "--model_base_path=" + os.getcwd() + "/../data/SavedModels/NCBI "
                                      "--port=9000 "
                                      "--rest_api_port=9001 "
                                      "--model_name=BioBert "],
                                     stdout=subprocess.DEVNULL,
                                     shell=True,
                                     preexec_fn=os.setsid)
    print("Tensorflow BioBert-diseases is starting")

    # A Flask server is started, for a front end to communicate with
    # Tensorflow server
    flask_server = subprocess.Popen(["export FLASK_ENV=development && flask run "
                                     "-h localhost -p 5000 "],
                                    stdout=subprocess.DEVNULL,
                                    shell=True,
                                    preexec_fn=os.setsid)
    print("Flask server is starting")

    while True:
        print("Type 'exit' and press 'enter' OR press CTRL+C to quit: ")
        in_str = input().strip().lower()
        if in_str == 'q' or in_str == 'exit':
            print('Shutting down all servers...')
            os.killpg(os.getpgid(tf_ic_server1.pid), signal.SIGTERM)
            os.killpg(os.getpgid(tf_ic_server2.pid), signal.SIGTERM)
            os.killpg(os.getpgid(flask_server.pid), signal.SIGTERM)
            print('Servers successfully shutdown!')
            break
        else:
            continue

except KeyboardInterrupt:
    print('Shutting down all servers...')
    os.killpg(os.getpgid(tf_ic_server1.pid), signal.SIGTERM)
    os.killpg(os.getpgid(tf_ic_server2.pid), signal.SIGTERM)
    os.killpg(os.getpgid(flask_server.pid), signal.SIGTERM)
    print('Servers successfully shutdown!')
