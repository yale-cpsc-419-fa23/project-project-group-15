import argparse
import sys
from app import app

#Start Server
def run_server(port):
    app.run(host='0.0.0.0', port=port, debug=True)

#Port command line processing
def handle_command_line():
    '''

    Returns: port number the server should run on

    '''
    parser = argparse.ArgumentParser(description="Server for the YUAG application")
    parser.add_argument("port", help="the port at which the server should listen")

    args = parser.parse_args()

    try:
        port=int(args.port)
    except ValueError:
        print('Port must be an int between 1 and 65536', file=sys.stderr)
        sys.exit(1)

    if port<=0:
        print('Port must be an int between 1 and 65536', file=sys.stderr)
        sys.exit(1)
    return port

#Driver Function
def main():
    port=handle_command_line()
    run_server(port)

if __name__ == "__main__":
    main()