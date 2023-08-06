import psutil
from colorama import Fore, Style

def get_cpu_load() -> int:
    return int(psutil.cpu_percent())


def get_total_ram() -> int:
    return int(psutil.virtual_memory().total / 1024 / 1024)


def get_ram_load() -> int:
    return int(psutil.virtual_memory().percent)


#def get_cpu
def pprint() -> None:
    print(f'{Fore.GREEN}cpu{Style.RESET_ALL}: {get_cpu_load()},\n' 
          f'{Fore.GREEN}total_ram{Style.RESET_ALL}: {get_total_ram()},\n'
          f'{Fore.GREEN}load_ram{Style.RESET_ALL}: {get_ram_load()}%'
    )

pprint()
