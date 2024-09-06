# env.py
import os
from pathlib import Path
import environ

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV = os.getenv("DJANGO_ENV", "local")
django_env = os.path.join(ROOT_DIR, f".envs/.{ENV}/.django")
postgres_env = os.path.join(ROOT_DIR, f".envs/.{ENV}/.postgres")

env = environ.Env()

if os.path.isfile(django_env):
    environ.Env.read_env(django_env)
if os.path.isfile(postgres_env):
    environ.Env.read_env(postgres_env)
