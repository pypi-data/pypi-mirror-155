import glob
import os


def awsconnect():
    pem_files = glob.glob("*.pem", recursive=True)
    if len(pem_files) != 0:
        pem_files = pem_files[0]
        os.chmod(f"./{pem_files}", 600)
        print(f'ssh -i "./{pem_files}" ubuntu@ec2-54-179-47-137.ap-southeast-1.compute.amazonaws.com')
