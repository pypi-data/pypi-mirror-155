""""Client library for folding proteins using Cradle's implementation of Alphafold.

Example::
    from cradlebio import alphafold

    creds_path = 'path to JSON firebase credentials obtained from https://auth.internal.cradle.bio/'
    fasta_file = 'path to fasta file containing proteins to be folded'
    sequences = alphafold.predict(creds_path, fasta_file)

    for sequence in sequences:
        print(f'PDB file for folded sequence {sequence.name} is {await sequence.pdb()}')
"""
from dataclasses import dataclass
from datetime import datetime
import logging
import hashlib
import os.path
from pathlib import Path
import tempfile
from tqdm import tqdm
from typing import Dict, List, Union
import urllib

from Bio import SeqIO
from google.cloud import firestore
from google.cloud import storage

from cradlebio import auth
from cradlebio import watch

CRADLE_GCS_BUCKET = 'cradle-bio.appspot.com'
JOBS = 'jobs'  # the name of the subcollection where jobs are stored in Firebase


class MsaException(Exception):
    """Indicator class for a server-side error during Multiple Sequence Alignment (MSA)"""
    pass


class PdbException(Exception):
    """Indicator class for a server-side error during sequence folding"""
    pass


class HttpOrGcsWrapper:
    """
    Simple wrapper around an http or gcs location that allows downloading the data at location to a file or string
    """
    location: str
    bucket: storage.Bucket

    def __init__(self, location: str, creds: auth.IdentityPlatformTokenCredentials):
        self.location = location
        gcs = storage.Client(credentials=creds.as_access_token_credentials())
        self.bucket = gcs.bucket(CRADLE_GCS_BUCKET)

    def to_file(self, fname) -> None:
        if str(self.location).startswith('https'):
            urllib.request.urlretrieve(self.location, fname)
        else:
            blob: storage.Blob = self.bucket.blob(str(self.location))
            blob.download_to_filename(fname)

    def to_string(self) -> str:
        if str(self.location).startswith('https'):
            with tempfile.NamedTemporaryFile() as f:
                urllib.request.urlretrieve(self.location, f.name)
                return open(f.name).read()
        else:
            blob: storage.Blob = self.bucket.blob(str(self.location))
            return blob.download_as_string().decode('UTF-8')


class Sequence:
    """A protein sequence that is being folded by AlphaFold"""

    _doc: firestore.DocumentReference
    job_id: str
    user_id: str
    seq: str
    id: str
    name: str
    _a3m_path: str
    _gcs_path: str
    _creds: auth.IdentityPlatformTokenCredentials

    def __init__(self, sequence_doc: firestore.DocumentReference, creds: auth.IdentityPlatformTokenCredentials):
        """
        The Firebase document corresponding to the current sequence. This is the document that is being watched
        in order to determine when the MSA job and the structure prediction jobs are done. The relevant fields are:
          a3m: set to the path of the MSA alignment results, after a successful MSA alignment (not set if MSA fails)
          a3m_error: an error message indicating why MSA failed (not set if MSA is successful)
          pdb: set to the path of the predicted PDB structure, after a successful structure prediction
              (not set if structure prediction fails)
          pdb_error: an error message indicating why structure prediction failed
              (not set if structure prediction is successful)
        Params:
            sequence_doc: the firebase document where the sequence data is stored
        """

        self._doc = sequence_doc
        self._a3m_path = None
        self._gcs_path = None
        self._pdbs = []
        self._creds = creds

    def __str__(self) -> str:
        snapshot = self._doc.get()
        return f'Id: {self.id}, {snapshot.to_dict()}'

    @property
    def id(self):
        return self._doc.id

    @property
    def name(self):
        return self._doc.get(['name']).get('name')

    @property
    def seq(self):
        return self._doc.get(['seq']).get('seq')

    @property
    def job_id(self):
        return self._doc.parent.parent.id

    @property
    def user_id(self):
        # the path to a sequence is 'users/<user_id>/jobs/<job_id>/sequences/<sequence_id>'
        return self._doc._path[-5]

    def to_dict(self):
        return self._doc.get().to_dict()

    def a3m(self) -> HttpOrGcsWrapper:
        """Wait for the MSA job to finish and return the path to the a3m data."""
        if not self._a3m_path:
            result = watch.field(self._doc, 'a3m', 'a3m_error')
            if 'a3m' in result:
                self._a3m_path = HttpOrGcsWrapper(result['a3m'], self._creds)
            elif 'a3m_error' in result:
                logging.error(f'Error performing MSA for {self.name}: {result["a3m_error"]}')
                raise MsaException(result["a3m_error"])
            else:
                logging.error(f'Unknown error performing MSA for {self.name}: no result provided by server')
                raise MsaException('No result provided by server')
        return self._a3m_path

    def pdbs(self) -> List[HttpOrGcsWrapper]:
        """"
        Wait for the folding to finish and return the contents of the resulting pdbs as strings,
        ranked by plddt score (best first).
        """
        # First wait for the MSA (and stop if the MSA resulted in an error)
        if not self._a3m_path:
            self.a3m()
        if self._gcs_path is None:
            pdb_result = watch.field(self._doc, 'pdbs', 'gcs_path', 'pdb_error')
            if 'pdb_error' in pdb_result:
                logging.error(f'Error folding {self.name}: {pdb_result["pdb_error"]}')
                raise PdbException(pdb_result["pdb_error"])
            self._gcs_path = pdb_result['gcs_path'] if 'gcs_path' in pdb_result else ''
            self._pdbs = []
            for p in pdb_result['pdbs']:
                if p.startswith('http'):
                    self._pdbs.append(HttpOrGcsWrapper(p, self._creds))
                else:
                    self._pdbs.append(HttpOrGcsWrapper(Path(self._gcs_path) / p, self._creds))
        return self._pdbs

    def pdb(self) -> HttpOrGcsWrapper:
        """ Return the PDB contents (as a string) with the highest plddt score for the given sequence """
        return self.pdbs()[0]


@dataclass
class Job:
    """A protein-folding job"""
    id: str
    job_data: Dict[str, any]
    sequences: List[Sequence]

    def __str__(self):
        return f'Job: {self.id}, {self.job_data}.\nSequences: {[s.name for s in self.sequences]}'


class Alphafold:
    def __init__(self, creds: auth.IdentityPlatformTokenCredentials):
        self.creds = creds

    @staticmethod
    def _get_job_id(fasta_file: str):
        """Build and return the job name string for a given fasta file that is being folded."""
        return datetime.today().strftime('%Y-%m-%d-%H:%M:%S_') + os.path.basename(fasta_file)

    @staticmethod
    def _md5(fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @staticmethod
    def _parse_fasta(fasta_file: str, db_client: firestore.Client, job_doc: firestore.DocumentReference,
                     creds: auth.IdentityPlatformTokenCredentials):
        """
        Parses the given fasta file and creates a Firebase document for each sequence under
        job_id/sequences/<sequence_name> with status 'PENDING'
        """
        logging.info(f'Parsing and uploading proteins in {fasta_file}')

        # parse the proteins in the FASTA file and write them as a batch to Firestore
        batch: firestore.WriteBatch = db_client.batch()
        fasta_sequences = SeqIO.parse(fasta_file, 'fasta')

        result: List[Sequence] = []
        sequence_set = set()
        count = 0
        for fasta in fasta_sequences:
            if fasta.seq in sequence_set:
                logging.warning(f'Duplicate sequence {fasta.id}. Ignoring.')
                continue
            sequence_set.add(fasta.seq)
            # since colabfold_search names sequences in the file starting with 0, we adopt
            # the same convention for convenience
            sequence_id = str(count)
            sequence_doc: firestore.DocumentReference = job_doc.collection('sequences').document(sequence_id)
            batch.create(sequence_doc, {'status': 'PENDING', 'seq': str(fasta.seq), 'name': str(fasta.id),
                                        'description': str(fasta.description)})
            result.append(Sequence(sequence_doc, creds))

            if (count + 1) % 500 == 0:  # a batch supports at most 500 operations
                batch.commit()
                batch = db_client.batch()
            count += 1
        batch.commit()
        logging.info(f'{len(sequence_set)}/{count} proteins successfully parsed and uploaded for processing.')
        return result

    def predict(self, fasta_file: str, show_progress=True) -> List[Sequence]:
        """
        Returns a list of sequences corresponding to the entries in fasta_file.
        The method synchronously copies the fasta file to GCS and then awaits until the fasta file is parsed
        on the server side before returning a list of Sequence instances corresponding to the entries in the fasta files.
        """
        if not os.path.exists(fasta_file):
            raise FileNotFoundError(f'Could not find FASTA file: {fasta_file}')

        db_client: firestore.Client = auth.get_client(self.creds)
        user_document: firestore.DocumentReference = auth.get_user_document(self.creds)

        md5sum = self._md5(fasta_file)
        identical_docs = user_document.collection(JOBS).where('md5sum', '==', md5sum).stream()
        for job_doc in identical_docs:
            logging.info(f'Found session {job_doc.to_dict()} with the same hash. Returning existing session.')
            if show_progress:
                tqdm(total=100, initial=100, unit='%', miniters=1, mininterval=0, ncols=110,
                     postfix='Done, duplicate').close()
            return [Sequence(sequence.reference, self.creds) for sequence in
                    job_doc.reference.collection('sequences').stream()]

        job_id = self._get_job_id(fasta_file)

        # create a new job for the user and a Firestore entry pointing at the FASTA file on GCS;
        # this signals the AFAAS sever to start processing the newly uploaded FASTA file
        job_doc = user_document.collection(JOBS).document(job_id)
        if job_doc.get().exists:
            raise RuntimeError(f'Duplicate session {job_id} when predicting structure for: {fasta_file}')
        if os.path.getsize(fasta_file) > 5e5:
            raise ValueError(f'Input file is too large: {fasta_file}. Max size is 500KB.')

        now = datetime.utcnow()
        job_doc.create({'creation_time': now, 'md5sum': md5sum})
        result = self._parse_fasta(fasta_file, db_client, job_doc, self.creds)

        # only update the status to PENDING after sequences are parsed, otherwise the server sees no sequences
        job_doc.update({'status': 'PENDING'})
        if show_progress:
            watch.add_progress_listener(job_doc, len(result))
        return result

    def get_jobs(self, active_only=True) -> List[Job]:
        """
        Return a list of alphafold jobs for the current user. Jobs are returned ordered by creation time, starting with
        the most recent one.
        Params:
            creds: Firebase credentials
            active: if True, only jobs that are currently running are shown
        """
        user_doc = auth.get_user_document(self.creds)
        # a sub-collection of all jobs for current user (list of documents)
        jobs_collection = user_doc.collection(JOBS)
        jobs: List[Job] = []
        for job in jobs_collection.stream():
            # using job.get('sequences') doesn't work with client credentials (requries privileged access with
            # a service account), so we manually query the path instead
            job_data = job.to_dict()
            # all sequences for current job (list of documents)
            sequences_collection = user_doc.collection(JOBS).document(job.id).collection('sequences')
            sequences = [Sequence(sequence.reference, self.creds) for sequence in sequences_collection.stream()]
            jobs.append(Job(job.id, job_data, sequences))
        if active_only:
            jobs = [j for j in jobs if
                    'status' in j.job_data and j.job_data['status'] not in ['DONE', 'MSA_FAILED', 'FOLDING_FAILED']]
        jobs.sort(key=lambda job: job.job_data['creation_time'], reverse=True)
        return jobs

    def get_job_by_id(self, job_id: str) -> Union[Job, None]:
        """Return the job with the given id for the authenticated user"""
        user_doc: firestore.DocumentReference = auth.get_user_document(self.creds)
        jobs_collection: firestore.CollectionReference = user_doc.collection(JOBS)  # all jobs for current user
        job: firestore.DocumentReference = jobs_collection.document(job_id)
        if not job.get().exists:
            return None
        sequences_collection: firestore.CollectionReference = job.collection(
            'sequences')  # all sequences for current job
        sequences = [Sequence(sequence.reference, self.creds) for sequence in sequences_collection.stream()]
        return Job(job_id, job.get().to_dict(), sequences)

    def search_jobs(self, keyword: str, active=True):
        """
        Search all jobs that match the given keyword.
        Params:
          - keyword string to search for in the job status, id, md5_sum or creation time.
          - active if, True, only jobs that are currently active are returned
        """
        jobs = self.get_jobs(active)
        if not keyword:
            return jobs
        result = []
        for j in jobs:
            data = j.job_data
            search_base = [data['status'], data['md5sum'], str(data['creation_time']), j.id]
            for s in search_base:
                if keyword in s:
                    result.append(j)
                    break
        return result
