import logging
import os
import pathlib
import pkg_resources
import pytest
import threading
from typing import Set
from unittest import mock

from google.cloud import firestore

from cradlebio import auth
from afaas.cache import cache
from cradlebio import watch

TEST_PATH = pathlib.Path(pkg_resources.resource_filename('afaas.tests.common', 'data'))
TEST_CREDENTIALS = TEST_PATH / 'test_creds.json'
TEST_SA_CREDENTIALS = TEST_PATH / 'test_server_creds.json'

SWISSPROT_PATH = pathlib.Path(pkg_resources.resource_filename('afaas.tests.cache', 'data')) / 'miniswissprot.fasta'

# this is setting up Application Default Credentials (ADC) with the service account
# afaas-test@cradle-bio.iam.gserviceaccount.com, with account data loaded from TEST_CREDENTIALS
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(TEST_SA_CREDENTIALS)


@pytest.fixture(scope='session')
def firestore_client():
    """ Returns a privileged client (uses test_server_creds.json via ADC) """
    return firestore.Client()


SEQ_COLLECTION = 'test_sequences'

_get_snapshot = cache.Cache._get_snapshot


def _get_snapshot_factory(latch: threading.Event, expected_seqs: Set[str]):
    def _mock_get_snapshot(self):
        """
        Does what the normal cache._get_snapshot does, and in addition it releases the global
        latch when all expected sequences were seen.
        """

        def on_snapshot(col_snapshot, changes, read_time):
            # first, call the normal snapshot handling
            _get_snapshot(self)(col_snapshot, changes, read_time)

            # now we are ready to check if the expected_seqs were seen
            for document, change in zip(col_snapshot, changes):
                if change.type in {watch.ChangeType.ADDED, watch.ChangeType.MODIFIED}:
                    expected_seqs.discard(document.get('seq'))
            if not expected_seqs and latch is not None:
                latch.set()

        return on_snapshot

    return _mock_get_snapshot


def empty_cache(cli: firestore.Client):
    """Clear the firebase case of all cached sequences."""
    sequences_collection = cli.collection(SEQ_COLLECTION)
    batch = cli.batch()
    for doc in sequences_collection.stream():
        batch.delete(doc.reference)
    batch.commit()


def cache_factory(client: firestore.Client, expected_seqs: Set[str]) -> cache.Cache:
    """Return a cache instance with 3 items"""
    sequences_collection = client.collection(SEQ_COLLECTION)
    latch = threading.Event()
    creds = auth.IdentityPlatformTokenCredentials.from_file(TEST_CREDENTIALS)
    with mock.patch.object(cache.Cache, '_get_snapshot', new=_get_snapshot_factory(latch, expected_seqs)):
        empty_cache(client)
        batch = client.batch()
        for i in range(3):
            d = sequences_collection.document()
            batch.create(d, {'location': f'users/{creds.uid}/test_jobs/job_1/sequences/1', 'seq': f'seq{i}', 'user': creds.uid})
        batch.commit()

        result = cache.Cache(client, sequence_collection_id=SEQ_COLLECTION, swissprot_path=SWISSPROT_PATH)
        result.latch = latch
        return result


@pytest.fixture(autouse=True)
def cleanup(firestore_client):
    """Make sure we clean up after ourselves"""
    yield
    empty_cache(firestore_client)


def test_load(firestore_client: firestore.Client):
    """Test that the initial Cache has the 3 items that were added at setup, plus the 2 in Swissprot"""
    under_test: cache.Cache = cache_factory(firestore_client, {'seq0', 'seq1', 'seq2'})
    under_test.latch.wait(timeout=10)
    assert len(under_test) == 5  # 3 we added now, plus the 2 in the fake Swissprot database
    for i in range(3):
        assert under_test.get('user_id', [f'seq{i}'])[f'seq{i}'].location == f'/users/user_id/jobs/job_id/pdb{i}'


def test_get_other_user(firestore_client: firestore.Client):
    """Test that the cache doesn't return the cached proteins for a different user"""
    under_test: cache.Cache = cache_factory(firestore_client, {'seq0', 'seq1', 'seq2'})
    under_test.latch.wait(timeout=10)
    assert len(under_test) == 5  # 3 we added now, plus the 2 in the fake Swissprot database
    for i in range(3):
        assert not under_test.get('other_user_id', [f'seq{i}'])


def __add_to_firebase(sequence_collection, user_id: str, seq: str, location: str):
    data = {'location': location, 'seq': seq, 'user': user_id}
    sequence_collection.add(data)


# TODO(dd): this test is flaky, most likely bc of a bug in the Python Firebase client library
# which sometimes fails to notify on_snapshot that seq3 was added
def test_add(firestore_client: firestore.Client):
    """Tests that directly adding a new folded sequence to Firebase notifies the cache"""
    under_test: cache.Cache = cache_factory(firestore_client, {'seq0', 'seq1', 'seq2', 'seq3'})
    logging.info('Adding sequence "seq3"')
    sequence_collection = firestore_client.collection(SEQ_COLLECTION)
    __add_to_firebase(sequence_collection, 'user_id', seq=f'seq3', location='/users/user_id/jobs/job_id/sequences/0')
    under_test.latch.wait(timeout=100000)  # TODO: set back to 10
    cached_results = under_test.get('user_id', ['seq3', 'seq4'])
    assert len(cached_results) == 1
    assert cached_results['seq3'] == cache.CachedData('user_id', '/users/user_id/jobs/job_id/sequences/0')


def test_get_swissprot(firestore_client: firestore.Client):
    under_test: cache.Cache = cache_factory(firestore_client, set())
    cached_data = under_test.get('', ['BANANANAS'])
    assert len(cached_data) == 1
    protein_data = cached_data['BANANANAS']
    assert '' == protein_data.user_id
    assert 'https://alphafold.ebi.ac.uk/files/AF-swissprot2-F1-model_v2.pdb' == protein_data.location
