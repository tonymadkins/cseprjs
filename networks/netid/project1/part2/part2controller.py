# Part 2 of UWCSE's Project 3
#
# based on Lab 4 from UCSC's Networking Class
# which is based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt

log = core.getLogger()


class Firewall (object):

  mactable = {}
  
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
  
    def installProtocolRule(self, dl_type, proto):
        msg = of.ofp_flow_mod()
        match = of.ofp_match()
        match.dl_type = dl_type
        match.nw_proto = proto
        msg.match = match
        action = of.ofp_action_output(port = of.OFPP_NORMAL)
        msg.actions.append(action)
        print('Adding flow for protocol : ' + str(proto))
        self.connection.send(msg)
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

    #add switch rules here
    # ICMP IPv4
    installProtocolRule(self, pkt.ethernet.IP_TYPE, pkt.ipv4.ICMP_PROTOCOL)
    # add rules to allow ALL ARP packets
    installProtocolRule(self, pkt.ethernet.ARP_TYPE, pkt.arp.REQUEST)
    installProtocolRule(self, pkt.ethernet.ARP_TYPE, pkt.arp.REPLY)
    installProtocolRule(self, pkt.ethernet.ARP_TYPE, pkt.arp.REV_REQUEST)
    installProtocolRule(self, pkt.ethernet.ARP_TYPE, pkt.arp.REV_REPLY)
    
  def _handle_PacketIn (self, event):
    """
    Packets not handled by the router rules will be
    forwarded to this method to be handled by the controller
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    print("Unhandled packet :" + str(packet.dump()))

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
