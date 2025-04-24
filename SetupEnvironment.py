"""
def pip_install():
    with cd(env.path):
        with prefix('source venv/bin/activate'):
            run('pip install -r requirements.txt')
"""