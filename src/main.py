from switcher import get_spammer


def main():
    inp = input("Enter the URL to spam: ")
    spammer = get_spammer(text=inp)
    if not spammer:
        print(
            f"Sorry, {inp} type links are not yet supported. "
            f"Please raise an issue regarding this on https://github.com/arin17bishwa/anon-msg-automator/issues."
        )
        return
    try:
        n = int(input("Enter number of times to spam(defaults to 1): "))
    except ValueError:
        n = 1
    print('Spamming.........')
    spammer.spam(n)


if __name__ == '__main__':
    main()
