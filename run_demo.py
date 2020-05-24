import os
import signal
import subprocess

# # Change directory to where your Flask's app.py is present
os.chdir("./demo")
tf_ic_server = ""
flask_server = ""

try:
    tf_ic_server = subprocess.Popen(["tensorflow_model_server " "--model_base_path=/home/arnoud/Documents/Sollicitaties/Ciphix/case/medical_entity_extraction/data/SavedModels/NCBI "
                                     "--port=9000 " "--rest_api_port=9001 " "--model_name=BioBert "],
                                    stdout=subprocess.DEVNULL,
                                    shell=True,
                                    preexec_fn=os.setsid)
    print("Tensorflow BioBert serving has started")

    flask_server = subprocess.Popen(["export FLASK_ENV=development && flask run"],
                                    stdout=subprocess.DEVNULL,
                                    shell=True,
                                    preexec_fn=os.setsid)
    print("Flask server has started")

    while True:
        print("Type 'exit' and press 'enter' OR press CTRL+C to quit: ")
        in_str = input().strip().lower()
        if in_str == 'q' or in_str == 'exit':
            print('Shutting down all servers...')
            os.killpg(os.getpgid(tf_ic_server.pid), signal.SIGTERM)
            os.killpg(os.getpgid(flask_server.pid), signal.SIGTERM)
            print('Servers successfully shutdown!')
            break
        else:
            continue
except KeyboardInterrupt:
    print('Shutting down all servers...')
    os.killpg(os.getpgid(tf_ic_server.pid), signal.SIGTERM)
    os.killpg(os.getpgid(flask_server.pid), signal.SIGTERM)
    print('Servers successfully shutdown!')


# "tensorflow_model_server --model_base_path=/home/arnoud/Documents/Sollicitaties/Ciphix/case/medical_entity_extraction/data/SavedModels/NCBI --port=9000 --rest_api_port=9001 --model_name=BioBert "
