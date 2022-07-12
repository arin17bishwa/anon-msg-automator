import argparse
from .modules import SecretM


def get_args():
    args = argparse.ArgumentParser()

    args.add_argument('-n', action='store_false',
                      help='Don\'t generate a colorscheme or set terminal colors')

    args.add_argument('-v', action='store_true',
                      help='Print version')
    args.add_argument(
        'platform',
        help='Give the platform name as mentioned in our documentation.',
    )

    args.add_argument(
        '--uid',
        help='Give the Unique Identification of the target user for the given platform. \nRefer to documentation for more details.',
        required=True
    )

    args.add_argument(
        '--repeat',
        help='Number of times to repeat the message sending.',
        default=1,
        type=int
    )

    args.add_argument(
        '--custom_text',
        help='Give a list possible text messages to send. Keep each message within quotation.',
        nargs='+'
    )

    return args.parse_args()


def main():
    args = get_args()
    platform = args.platform
    # print(args)
    messengers = {
        'secretm': SecretM
    }
    if platform not in messengers:
        print('The requested platform is not supported yet. Please raise an issue in GitHub to request addition.')
        return
    messenger = messengers[platform](
        uid=args.uid,
        messages={'custom_text': args.custom_text} if args.custom_text else None
    )
    messenger.post(n=args.repeat)


if __name__ == '__main__':
    main()
