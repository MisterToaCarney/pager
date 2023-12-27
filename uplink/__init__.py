import firebase_admin
import firebase_admin.firestore_async
from google.cloud.firestore_v1.async_document import AsyncDocumentReference
import config
import datetime

from dataclasses import dataclass, asdict
from postprocess.ambo import JobAssignment
from postprocess.pocsag import ParsedPocsagPage
from postprocess.flex_next import ParsedFlexPage
from postprocess.fire import FireAssignment

@dataclass
class FirestoreJobAssignment:
    message: str
    unit: str
    priority: str
    type_code: str
    type_plaintext: str
    address: str
    date: datetime.datetime
    page_ref: AsyncDocumentReference

@dataclass
class FirestoreFireAssignment:
    message: str
    units: list[str]
    type: str
    address: str
    xstreet: str
    details: str
    job_id: int
    date: datetime.datetime
    page_ref: AsyncDocumentReference

@dataclass
class FirestorePagerMessage:
    date: datetime.datetime
    message: str

cred = firebase_admin.credentials.Certificate(config.args.service_account)
firebase_admin.initialize_app(cred)
client = firebase_admin.firestore_async.client()

async def add_page(page: ParsedPocsagPage | ParsedFlexPage):
    entry = FirestorePagerMessage(date=page.date, message=page.message)
    col = client.collection("pages")
    update_time, ref = await col.add(document_data=asdict(entry))
    return ref

async def add_job_assignment(date, page_ref: AsyncDocumentReference, job: JobAssignment):
    col = client.collection("ambo_assignments")
    entry = FirestoreJobAssignment(**asdict(job), date=date, page_ref=page_ref)
    update_time, ref = await col.add(document_data=asdict(entry))
    return ref
    
async def add_fire_assignment(date, page_ref: AsyncDocumentReference, assignment: FireAssignment):
    col = client.collection("fire_assignments")
    entry = FirestoreFireAssignment(**asdict(assignment), date=date, page_ref=page_ref)
    update_time, ref = await col.add(document_data=asdict(entry))
    return ref
