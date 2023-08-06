from colorama import Fore


def kavian_info() -> None:
    print(Fore.GREEN + 'Hello, My name is Kavian and I\'m currently 26 years old')


def greet(msg: str = None) -> None:
    if msg is None:
        msg = input()
    match msg.lower().split():
        case ['hello' | 'salam', str(name)]:
            print(Fore.BLUE, "Hello", name, "Welcome")
        case name, int(age) if int(age) < 10:
            print(f"{Fore.BLUE}happy birthday {name} you are {age} years old and little")
        case name, int(age) if int(age) > 10:
            print(f"{Fore.BLUE}happy birthday {name} you are {age} years old and big")
        case [str('bye')]:
            print(Fore.BLUE, "Bye")
        case [name]:
            print("Welcome", name)
        case ['hello', *_, 'bye']:
            print("Why are you leaving so soon")
        case ['salam', _, _, name]:
            print('salam bar to ey', name)
        case ['bye', *extra, 'smth']:
            print(Fore.RED + 'bye', extra)
        case _:
            print(Fore.RED + "fuck you")


if __name__ == '__main__':
    kavian_info()
