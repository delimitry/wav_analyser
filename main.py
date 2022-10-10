import argparse


def main():
    """Main"""
    parser = argparse.ArgumentParser(description='Wav file analyser')
    parser.add_argument('filename', type=str, help='Wav file')

    args = parser.parse_args()
    # TODO: read wave file


if __name__ == '__main__':
    main()
