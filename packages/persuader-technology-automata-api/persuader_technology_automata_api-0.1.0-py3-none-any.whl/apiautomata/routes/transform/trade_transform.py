from typing import List

from fastapi import APIRouter
from tradetransformrepo.TradeTransform import TradeTransform
from tradetransformrepo.repository.TradeTransformRepository import TradeTransformRepository

from apiautomata.holder.ItemHolder import ItemHolder

router = APIRouter()


@router.get('/transform/trade', response_model=List[TradeTransform])
async def get_all_trade_transforms():
    trade_transform_repository = ItemHolder.get_entity(TradeTransformRepository)
    return trade_transform_repository.retrieve()


@router.put('/transform/trade')
async def create_trade_transform(trade_transform: TradeTransform):
    trade_transform_repository = ItemHolder.get_entity(TradeTransformRepository)
    trade_transform_repository.append(trade_transform)
    return trade_transform
