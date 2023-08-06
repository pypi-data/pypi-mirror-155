import dataclasses
from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.TransformStampedMessage import TransformStampedMessage


@dataclasses.dataclass
class PoseRequestMessage(CBorMessage):
    pose: TransformStampedMessage
    name: str
    pos_tolerance: float
    rot_tolerance: float
