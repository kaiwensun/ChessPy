MSG_TYPE_CONTROL = 'msg_type_ctrl'
MSG_TYPE_CHESSMOVE = 'msg_type_chessmove'
MSG_TYPE_NOP = 'msg_type_nop'
MSG_TYPE_HEARTBEAT = 'msg_type_heartbeat'
MSG_TYPE_UNDOREQ = 'msg_type_undoReq'
MSG_TYPE_REPLYUNDOREQ = 'msg_type_replyUndoReq'
MSG_TYPE_DRAWREQ = 'msg_type_drawReq'
MSG_TYPE_REPLYDRAWREQ = 'msg_type_replyDrawReq'
MSG_TYPE_RESIGNREQ = 'msg_type_resignReq'
MSG_TYPE_MATCHEND = 'msg_type_matchEnd'


# tell the other player "I am about to leave the match!"
MSG_CONST_LEFT = 'msg_const_left'

# tell the other player "I joined the match!"
MSG_CONST_JOIN = 'msg_const_join'


# TODO: all messages should have type and data
# message = {
#     'type': msg_meta.MSG_TYPE_CONTROL,
#     'data': msg_meta.MSG_CONST_LEFT
# }
