#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class AssignPlayMarketTransaction(TLObject):  # type: ignore
    """Telegram API method.

    Details:
        - Layer: ``143``
        - ID: ``4FAA4AED``

    Parameters:
        purchase_token: ``str``

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["purchase_token"]

    ID = 0x4faa4aed
    QUALNAME = "functions.payments.AssignPlayMarketTransaction"

    def __init__(self, *, purchase_token: str) -> None:
        self.purchase_token = purchase_token  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AssignPlayMarketTransaction":
        # No flags
        
        purchase_token = String.read(b)
        
        return AssignPlayMarketTransaction(purchase_token=purchase_token)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.purchase_token))
        
        return b.getvalue()
