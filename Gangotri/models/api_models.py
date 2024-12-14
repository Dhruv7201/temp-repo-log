class VendResponse(object):
    def __init__(self, MachineNo, SR_No, VendingStatus, OPDD_ID):
        self.MachineNo = MachineNo
        self.SR_No = SR_No
        self.VendingStatus = VendingStatus
        self.OPDD_ID = OPDD_ID


class VendResponseArray(object):
    def __init__(self, itemlist):
        self.itemlist = itemlist
