import logging
from typing import Dict, List, NamedTuple

from cradlebio import watch

from Bio import SeqIO
from google.cloud import firestore


class CachedData(NamedTuple):
    user_id: str  # the firebase user id of the user who owns the data
    # the location of the cached data: either a Firebase path (if we folded it before)
    # or a Swissprot URL (if cached in Swissprot)
    location: str


class Cache:
    """
    Caches already folded proteins.
    The cache supports two data sources: SwissProt and AFAAS's previously folded proteins.
    Caching assumes all folding happens with default parameters, i.e. no parameter-specific caching is supported (yet).
    """

    def __init__(self, db_client: firestore.Client, sequence_collection_id='sequences',
                 swissprot_path: str = '/opt/colabfold/databases/uniprot_sprot.fasta'):
        """
        Creates a new cache instance and loads the data from the given Firestore database.
        Parameters:
            db_client: Firestore client, authenticated with a privileged service account
            sequence_collection_id: the Firestore collection id where sequences are cached
            mmseqs_path: path to the mmseqs binary (used for searching against the swissprot DB)
            cache_db: path to the mmseqs database to search against (e.g. Swissprot, or some test database when testing)
        """

        self.cache: Dict[str:CachedData] = {}
        self.db_client = db_client
        self.swissprot_path = swissprot_path
        self.sequence_collection = db_client.collection(sequence_collection_id)
        self.sequence_collection.on_snapshot(self._get_snapshot())
        self._load_swissprot()

    def _load_swissprot(self):
        logging.info(f'Loading Swissprot entries from: {self.swissprot_path}')

        fasta_sequences = SeqIO.parse(open(self.swissprot_path), 'fasta')
        counter = 0
        for fasta in fasta_sequences:
            protein = str(fasta.seq)
            id = fasta.id.split('|')[1]
            self.cache[protein] = CachedData('', f'https://alphafold.ebi.ac.uk/files/AF-'
                                                 f'{id}-F1-model_v2.pdb')
            counter += 1
        logging.info(f'Loaded {counter} entries from Swissprot.')

    def _get_snapshot(self):
        def on_snapshot(col_snapshot: List[firestore.DocumentSnapshot], changes: List[watch.DocumentChange], _):
            try:
                for document, change in zip(col_snapshot, changes):
                    if change.type in {watch.ChangeType.ADDED}:
                        seq = document.get('seq')
                        user_id = document.get('user')
                        if seq in self.cache and self.cache[seq].user_id == user_id:
                            logging.info(f'Sequence seq[:20]... already in cache for user {user_id}')
                            continue
                        self.cache[seq] = CachedData(user_id, document.get('location'))
                        logging.info(f'Sequence {document.get("seq")[:20]}... added to cache')
            except Exception as e:
                logging.error(str(e))
                raise

        return on_snapshot

    def get(self, user_id: str, proteins: List[str]) -> Dict[str, CachedData]:
        """ Looks up the list of proteins in the cache, and returns the folding, if available. """
        result = {}
        for protein in proteins:
            # make sure we only return the protein if it's owned by the user or if it has no owner
            if protein in self.cache and (self.cache[protein].user_id == user_id or self.cache[protein].user_id == ''):
                result[protein] = self.cache[protein]
        return result

    def __len__(self):
        return len(self.cache)
