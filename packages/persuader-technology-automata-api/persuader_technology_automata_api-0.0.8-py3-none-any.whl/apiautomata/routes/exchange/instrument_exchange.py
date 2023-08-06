from typing import List

from core.exchange.InstrumentExchange import InstrumentExchange
from exchangerepo.repository.InstrumentExchangeRepository import InstrumentExchangeRepository
from fastapi import APIRouter

from apiautomata.holder.ItemHolder import ItemHolder

router = APIRouter()


@router.get('/exchange/instrument', response_model=List[InstrumentExchange])
async def exchange_instruments():
    instrument_exchange_repository = ItemHolder.get_entity(InstrumentExchangeRepository)
    holder = instrument_exchange_repository.retrieve()
    return holder.get_all()


@router.post('/exchange/instrument')
async def add_exchange_instrument(instrument_exchange: InstrumentExchange):
    instrument_exchange_repository = ItemHolder.get_entity(InstrumentExchangeRepository)
    instrument_exchange_repository.append_store(instrument_exchange)
    return instrument_exchange
