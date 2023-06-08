import firebase_admin
import firebase_admin.firestore_async
import config
import datetime

from dataclasses import dataclass, asdict
from postprocess.ambo import JobAssignment

@dataclass
class FirestoreJobAssignment:
    message: str
    unit: str
    priority: str
    type_code: str
    type_plaintext: str
    address: str
    date: datetime.datetime
    

cred = firebase_admin.credentials.Certificate(config.args.service_account)
firebase_admin.initialize_app(cred)
client = firebase_admin.firestore_async.client()

async def add_job_assignment(date, job: JobAssignment):
    col = client.collection("tests")
    entry = FirestoreJobAssignment(**asdict(job), date=date)
    await col.add(document_data=asdict(entry))
    