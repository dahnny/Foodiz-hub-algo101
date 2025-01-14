from pyteal import *


class Meal:
    class Variables:
        name = Bytes("NAME")
        image = Bytes("IMAGE")
        price = Bytes("PRICE")
        description = Bytes("DESCRIPTION")

    def application_creation(self):
        return Seq([
            Assert(Txn.application_args.length() == Int(4)),
            Assert(Txn.note() == Bytes("foodiz:uv1")),
            Assert(Btoi(Txn.application_args[2]) > Int(0)),
            App.globalPut(self.Variables.name, Txn.application_args[0]),
            App.globalPut(self.Variables.image, Txn.application_args[1]),
            App.globalPut(self.Variables.price, Btoi(Txn.application_args[2])),
            App.globalPut(self.Variables.description, Txn.application_args[3]),
            Approve()
        ])

    def application_deletion(self):
        return Return(Txn.sender() == Global.creator_address())

    def application_start(self):
        return Cond(
            [Txn.application_id() == Int(0), self.application_creation()],
            [Txn.on_completion() == OnComplete.DeleteApplication,
             self.application_deletion()],
        )

    def approval_program(self):
        return self.application_start()

    def clear_program(self):
        return Return(Int(1))
