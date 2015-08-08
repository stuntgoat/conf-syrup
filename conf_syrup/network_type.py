from commands import getoutput


def NetworkFromPrefix(val):
    """
    Return the network with the network prefix given.

    """

    ifaces = getoutput('hostname -I')  # *nix only.
    sifaces = ifaces.strip().split()
    for iface in sifaces:
        if iface.startswith(val):
            return iface
