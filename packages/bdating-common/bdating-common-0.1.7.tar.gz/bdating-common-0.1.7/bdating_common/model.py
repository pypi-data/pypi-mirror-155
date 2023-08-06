
from typing import List, Optional
from pydantic import BaseModel

# data model


class Location(BaseModel):
  lat: float
  lon: float


class BaseProfile(BaseModel):
  wallet: str
  name: str


class ProducerProfile(BaseProfile):
  address: str
  location: Location
  bio: Optional[str] = ""
  rate_aud: int = 150


class ConsumerProfile(BaseProfile):
  pass


class TimeSlot(BaseModel):
  wallet: str  # the producer
  slot_id: int  # the slot id, YYYYmmddXX
  name: str
  address: str
  location: Location
  bio: Optional[str] = ""
  rate_aud: int = 150


class Booking(TimeSlot):  # booking to a timeslot
  consumer_wallet: str
  num_slots: int = 1
  price: int
  book_time: int  # epoch second of booked


class Order(Booking):
  confirm_random_code: str
  confirm_random_code_time: str
  confirm_time: int
  finish_time: int


# response model


class SingleProducerResponse(ProducerProfile):
  pass


class SingleConsumerResponse(ConsumerProfile):
  pass


class SingleTimeSlotResponse(TimeSlot):
  pass


class SingleBookingResponse(Booking):
  pass


class SingleOrderResponse(Order):
  pass


class ProducerListResponse(BaseProfile):
  results: List[ProducerProfile] = []
  start: Optional[int]
  total_size: Optional[int]
  next_cursor: Optional[str]


class TimeSlotListResponse(BaseProfile):
  results: List[TimeSlot] = []
  start: Optional[int]
  total_size: Optional[int]
  next_cursor: Optional[str]


class BookingListResponse(BaseProfile):
  results: List[Booking] = []
  start: Optional[int]
  total_size: Optional[int]
  next_cursor: Optional[str]


class OrderListResponse(BaseProfile):
  results: List[Booking] = []
  start: Optional[int]
  total_size: Optional[int]
  next_cursor: Optional[str]

# general model


class HealthResponse(BaseModel):
  status: str
