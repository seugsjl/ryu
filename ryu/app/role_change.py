
import logging

from ryu.ofproto import ether
from ryu.ofproto import inet
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ofproto_v1_3_parser
from ryu.lib import ofctl_v1_0
from ryu.lib import ofctl_v1_2
from ryu.lib import ofctl_v1_3
from ryu.lib import hub

LOG = logging.getLogger('ryu.lib.role_change')

def send_role_request(dp, waiters, change, generation_id):
    changeRole = dp.ofproto.OFPCR_ROLE_NOCHANGE
    if change == "NOCHANGE":
        changeRole = dp.ofproto.OFPCR_ROLE_NOCHANGE
    elif change == "EQUAL":
        changeRole = dp.ofproto.OFPCR_ROLE_EQUAL
    elif change == "MASTER":
        changeRole = dp.ofproto.OFPCR_ROLE_MASTER
    elif change == "SLAVE":
        changeRole = dp.ofproto.OFPCR_ROLE_SLAVE
    else:
         LOG.debug('Unsupported Role %s' % (change))
    
    g_id = long(generation_id,10) 
    req = dp.ofproto_parser.OFPRoleRequest(dp, changeRole,g_id)
    msgs = [] 
    ofctl_v1_3.send_stats_request(dp, req, waiters, msgs)
    length = len(msgs)
    if length == 0:
    	info = '%s'%(generation_id)
    	return {'error':info}
    msg = msgs[0]
    dp = msg.datapath
    ofp = dp.ofproto

    if msg.role == ofp.OFPCR_ROLE_NOCHANGE:
        role = 'NOCHANGE'
    elif msg.role == ofp.OFPCR_ROLE_EQUAL:
        role = 'EQUAL'
    elif msg.role == ofp.OFPCR_ROLE_MASTER:
        role = 'MASTER'
    elif msg.role == ofp.OFPCR_ROLE_SLAVE:
        role = 'SLAVE'
    else:
        role = 'UNKNOWN'
    d = {'dpid':str(dp.id),
    	   'role':role,
    	   'generation_id':str(msg.generation_id)
    	   }
    return d;    