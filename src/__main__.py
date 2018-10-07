from stubbed.flask_wrapper import Server

if __name__ == "__main__":
    server = Server(host="0.0.0.0", port=9694)
    server.run()
