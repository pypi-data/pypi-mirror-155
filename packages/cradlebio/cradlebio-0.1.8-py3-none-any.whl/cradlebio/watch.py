import logging
import threading
from typing import Any, List

from google.cloud import firestore
from google.cloud.firestore_v1.watch import DocumentChange, ChangeType
from tqdm import tqdm
from proto.datetime_helpers import DatetimeWithNanoseconds


def add_progress_listener(job_doc: firestore.DocumentReference, seq_count: int):
    """ Listens to changes on the job document and sequences in firestore and updates a progress bar. """
    bar = tqdm(total=100, unit='%', miniters=1, mininterval=0, ncols=110)

    def job_callback(docs: List[firestore.DocumentSnapshot],
                     changes: List[DocumentChange],
                     _: DatetimeWithNanoseconds):
        for document, change in zip(docs, changes):
            if change.type in {ChangeType.MODIFIED}:
                # logging.info(f'on_snapshot() called with {document.to_dict()}')
                data = document.to_dict()
                if 'status' not in data:
                    continue
                status = data['status']
                if status == 'MSA_QUEUE':
                    bar.set_postfix_str('MSA Queue'.ljust(34))
                    bar.update()
                elif status == 'MSA_RUNNING':
                    data = document.to_dict()
                    if 'msa_progress' not in data:
                        bar.set_postfix_str('MSA Running'.ljust(34))
                        bar.update()
                    else:
                        bar.set_postfix_str(data['msa_progress']['status'].ljust(34))
                        bar.n = data['msa_progress']['current']
                        bar.update(0)
                elif status == 'MSA_Error':
                    bar.set_postfix_str('MSA Error  ')
                    bar.n = 100
                    bar.update(0)  # force refresh
                    bar.close()
                elif status == 'MSA_COMPLETE':
                    bar.set_postfix_str('MSA Complete'.ljust(34))
                    bar.n = 50
                    bar.update(0)
                elif status == 'FOLD_QUEUE':
                    bar.set_postfix_str('Fold Queue'.ljust(34))
                    bar.update()
                elif status == 'FOLDING':
                    bar.set_postfix_str('Folding'.ljust(34))
                    bar.update()
                elif status == 'DONE' or status == 'MSA_FAILED' or status == 'FOLDING_FAILED':
                    bar.set_postfix_str(status.ljust(34))
                    bar.n = 100
                    bar.update(0)
                    bar.close()

    sequences: firestore.CollectionReference = job_doc.collection('sequences')
    folding_progress = [0 for _ in range(seq_count)]

    def seq_callback(docs: List[firestore.DocumentSnapshot],
                     changes: List[DocumentChange],
                     _: DatetimeWithNanoseconds):
        for document, change in zip(docs, changes):
            if change.type in {ChangeType.MODIFIED}:
                data = document.to_dict()
                if 'progress' not in data:
                    return
                progress = data['progress']['current']
                folding_progress[int(document.id)] = progress
                if progress > 0:
                    current_progress = sum(folding_progress) / (seq_count * data['progress']['total'])
                    bar.n = 50 + (50 * current_progress)
                    bar.update(0)  # force refresh
                action = 'Folding' if progress % 2 == 0 else 'Amber relax'
                model = progress // 2 + 1
                bar.set_postfix_str(f'Sequence {document.id}, model {model}/5, {action}'.ljust(34))

    job_doc.on_snapshot(job_callback)
    sequences.on_snapshot(seq_callback)


def field(doc: firestore.DocumentReference, *field_names: str) -> Any:
    """
    Watches the given fields in the document for changes and returns when one of the desired
    fields has changed.
    """
    event = threading.Event()
    retval = None

    def callback(docs: List[firestore.DocumentSnapshot],
                 changes: List[DocumentChange],
                 _: DatetimeWithNanoseconds):
        for document, change in zip(docs, changes):
            if change.type in {ChangeType.ADDED, ChangeType.MODIFIED}:
                data = document.to_dict()
                result = {field_name: data[field_name] for field_name in field_names if field_name in data}
                if result:
                    nonlocal retval
                    retval = result
                    event.set()

    doc.on_snapshot(callback)

    result = doc.get(field_names).to_dict()
    if result:  # the document already has the fields we are looking for
        return result

    event.wait()
    return retval
