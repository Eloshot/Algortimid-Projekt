# Algortimid-Projekt

## Süsteemi nõuded

- Python 3.11

## Arenduskeskkond

### pip venv

Pythoni virtuaalkeskkonna nullist loomiseks kasutame

```bash
make setup
# reload terminal to activate virtual environment
```

Kui venv ei aktiveeru ise siis

```bash
source .venv/bin/activate
```

Uusi librareid lisades (`pip install <my_lib>`) peab olema venv aktiveeritud ning pärast installimist peab library-d lisama requirements.txt faili, et teised arendajad saaksid lihtsalt vajalikud library-d installida.

```bash
make requirements
```

### Käivitamine

```bash
make run
# or
python 'snake game.py'
```
