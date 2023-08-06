def get_client_public_ip_address():
    """
    Reads client machine ip

    @return (string|bool) ipAddress"""
    import socket

    ipAddress = None

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ipAddress = s.getsockname()[0]
        s.close()
    except Exception:
        print("Could not resolve client ip")

    return ipAddress
