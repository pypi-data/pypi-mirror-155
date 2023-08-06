import argparse
from whttp import HTTPClient


def main():
    parser = argparse.ArgumentParser(description="Perform HTTP GET on url ")
    parser.add_argument("url", help="The url to be used on the HTTP request")
    args = parser.parse_args()
    client = HTTPClient()
    reply = client.get(args.url)
    print(reply.text)


if __name__ == "__main__":
    main()
