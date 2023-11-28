class ReceiverProcess:
    """ Represent the receiver process in the application layer  """
    __buffer = list()

    @staticmethod
    def deliver_data(data):
        """ deliver data from the transport layer RDT receiver to the application layer
        :param data: a character received by the RDT RDT receiver
        :return: no return value
        """
        ReceiverProcess.__buffer.append(data)
        return

    @staticmethod
    def get_buffer():
        """ To get the message the process received over the network
        :return:  a python list of characters represent the incoming message
        """
        return ReceiverProcess.__buffer


class RDTReceiver:
    """" Implement the Reliable Data Transfer Protocol V2.2 Receiver Side """

    def __init__(self):
        self.sequence = '0'

    @staticmethod
    def is_corrupted(packet):
        """ Check if the received packet from sender is corrupted or not
            :param packet: a python dictionary represent a packet received from the sender
            :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted
        """
        # TODO provide your own implementation
        if ord(packet['data']) == packet['checksum']:
            return False
        else:
            return True

    @staticmethod
    def is_expected_seq(rcv_pkt, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
         :param rcv_pkt: a python dictionary represent a packet received by the receiver
         :param exp_seq: the receiver expected sequence number '0' or '1' represented as a character
         :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        # TODO provide your own implementation
        if rcv_pkt['sequence_number'] == exp_seq:
            return True
        else: 
            return False


    @staticmethod
    def make_reply_pkt(seq, checksum):
        """ Create a reply (feedback) packet with to acknowledge the received packet
        :param seq: the sequence number '0' or '1' to be acknowledged
        :param checksum: the checksum of the ack the receiver will send to the sender
        :return:  a python dictionary represent a reply (acknowledgement)  packet
        """
        reply_pck = {
            'ack': seq,
            'checksum': checksum
        }
        return reply_pck

    def rdt_rcv(self, rcv_pkt):
        """  Implement the RDT v2.2 for the receiver
        :param rcv_pkt: a packet delivered by the network layer 'udt_send()' to the receiver
        :return: the reply packet
        """

        # TODO provide your own implementation
        if rcv_pkt:
            print("Receiver: expecting seq_num:"+ str(self.sequence))
            if not RDTReceiver.is_corrupted(rcv_pkt):

                
                print("Receiver: reply with: {'ack':" +str(rcv_pkt['sequence_number'])+", 'checksum':" + str(ord(rcv_pkt['sequence_number']))+"}")
            else:
                print("network_layer: corruption occured {'sequence_number':" +str(rcv_pkt['sequence_number'])+", 'data':"+str(rcv_pkt['data'])+", 'checksum':" + str(rcv_pkt['checksum']))
                if rcv_pkt['sequence_number'] == '0':
                    self.sequence = '1'
                elif rcv_pkt['sequence_number'] == '1':
                    self.sequence = '0'
                print("Receiver: reply with: {'ack':" +str(self.sequence)+", 'checksum':" + str(ord(self.sequence))+"}")

            # deliver the data to the process in the application layer
            ReceiverProcess.deliver_data(rcv_pkt['data'])

            reply_pkt = RDTReceiver.make_reply_pkt(self.sequence,ord(self.sequence))
            return reply_pkt

        #return None
