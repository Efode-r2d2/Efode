import math
import operator
import sqlite3
from bisect import bisect_left, bisect_right
from collections import defaultdict

import numpy as np


def create_tables(conn):
    """
    A function to create required tables to store hashes, audio information and raw data of each triplet.

    Parameters:
        conn (String): connection string to the sqlite database.

    """
    conn.executescript("""
                CREATE VIRTUAL TABLE
                IF NOT EXISTS Hashes USING rtree(
                    id,
                    minNewP3x, maxNewP3x,
                    minNewP3y, maxNewP3y);
                CREATE TABLE
                IF NOT EXISTS Audios(
                    id INTEGER PRIMARY KEY,
                    audio_title TEXT);
                CREATE TABLE
                IF NOT EXISTS Triplets(
                    hash_id INTEGER PRIMARY KEY,
                    audio_id INTEGER,
                    P1x INTEGER, P1y INTEGER,
                    P2x INTEGER, P2y INTEGER,
                    FOREIGN KEY(hash_id) REFERENCES Hashes(id),
                    FOREIGN KEY(audio_id) REFERENCES Audios(id));
                CREATE TABLE
                IF NOT EXISTS Peaks(
                    audio_id INTEGER, Px INTEGER, Py INTEGER,
                    PRIMARY KEY(audio_id, Px, Py),
                    FOREIGN KEY(audio_id) REFERENCES Audios(id));""")


def store_audio(cursor, audio_title):
    """
    A function to store audio information.

    Parameters:
        cursor : current cursor of the database.
        audio_title (String): Title of the audio.
    Returns:
        int : the id of the last row.

    """
    cursor.execute("""INSERT INTO Audios
                         VALUES (null,?)""", (audio_title,))
    return cursor.lastrowid


def record_exists(cursor, audio_title):
    """
    A function to check whether a given audio title exist in a database or not.

    Parameters:
        cursor : current cursor of the database.
        audio_title (String): title of the audio.

    Returns:
        Boolean: True if the given audio title exist, False if the given audio title doesn't exist.

    """
    cursor.execute("""SELECT id
                           FROM Audios
                          WHERE audio_title = ?""", (audio_title,))
    record_id = cursor.fetchone()
    if record_id is None:
        return False
    else:
        print("record already exists...")
        return True


def store_hash(cursor, geo_hash):
    """
    A function to store triple point based geometric hashes into the database.

    Parameters:
        cursor : the current cursor of the database.
        geo_hash (List): geometric hash computed using the association of three spectral peaks.

    """
    cursor.execute("""INSERT INTO Hashes
                         VALUES (null,?,?,?,?)""",
                   (geo_hash[0], geo_hash[0], geo_hash[1], geo_hash[1]))


def radius_nn(cursor, geo_hash, e=0.01):
    """
    A function to find nearest neighbors for a given geometric hash.

    Parameters:
        cursor : the current cursor of the database.
        geo_hash (List) : geometric hash computed using the association of three spectral peaks.
        e : maximum allowed range for nearest neighbor search.

    """
    cursor.execute("""SELECT id FROM Hashes
                  WHERE minNewP3x >= ? AND maxNewP3x <= ?
                    AND minNewP3y >= ? AND maxNewP3y <= ?""",
                   (geo_hash[0] - e, geo_hash[0] + e,
                    geo_hash[1] - e, geo_hash[1] + e))


def find_hash(cursor, hash_value, e=0.01):
    """
    A function to retrieve all the matching hashes with in the range of e.

    Parameters:
        cursor : The current cursor of the database.
        hash_value (tuple): A hash extracted from a query audio.
        e (float): A look up radius for the r-tree.

    """
    cursor.execute("""SELECT Triplets.P1x,Triplets.P1y,Triplets.P2x,Triplets.P2y,Triplets.audio_id FROM Triplets INNER JOIN Hashes
                    ON Triplets.hash_id = Hashes.id
                  WHERE Hashes.minNewP3x >= ? AND Hashes.maxNewP3x <= ?
                    AND Hashes.minNewP3y >= ? AND Hashes.maxNewP3y <= ?""",
                   (hash_value[0] - e, hash_value[0] + e,
                    hash_value[1] - e, hash_value[1] + e))


def store_triplet(cursor, triplet, audio_id):
    """

    :param cursor:
    :param triplet:
    :param audio_id:
    :return:
    """
    hash_id = cursor.lastrowid
    values = (hash_id, audio_id, int(triplet[0]), int(triplet[1]), int(triplet[2]), int(triplet[3]))
    cursor.execute("""INSERT INTO Triplets
                         VALUES (?,?,?,?,?,?)""", values)


def lookup_triplets(conn, hash_ids):
    cursor = conn.cursor()
    cursor.execute("""SELECT P1x,P1y,P2x,P2y,audio_id FROM Triplets
                          WHERE hash_id=?""", hash_ids)
    row = cursor.fetchone()
    cursor.close()
    return [row[0], row[1], row[2], row[3]], row[4]


def bin_times(l, bin_width=20, ts=4):
    """
    Takes list of rough offsets and bins them in time increments of
    binwidth. These offsets are stored in a dictionary of
    {binned time : [list of scale factors]}. Binned time keys with
    less than Ts scale factor values are filtered out.
    """
    d = defaultdict(list)
    for rough_offset in l:
        div = rough_offset[0] / bin_width
        binname = int(math.floor(div) * bin_width)
        d[binname].append((rough_offset[1][0], rough_offset[1][1]))
    return {k: v for k, v in d.items() if len(v) >= ts}


def filter_candidates(cursor, query_triplet, filtered, tolerance=0.31, e_fine=1.8):
    for reference_triplet in cursor:
        # Rough pitch coherence:
        #   1/(1+e) <= queAy/canAy <= 1/(1-e)
        if not 1 / (1 + tolerance) <= query_triplet[1] / reference_triplet[1] <= 1 / (1 - tolerance):
            continue
        # X transformation tolerance check:
        #   sTime = (queBx-queAx)/(canBx-canAx)
        sTime = (query_triplet[2] - query_triplet[0]) / (reference_triplet[2] - reference_triplet[0])
        if not 1 / (1 + tolerance) <= sTime <= 1 / (1 - tolerance):
            continue
        # Y transformation tolerance check:
        #   sFreq = (queBy-queAy)/(canBy-canAy)
        sFreq = (query_triplet[3] - query_triplet[1]) / (reference_triplet[3] - reference_triplet[1])
        if not 1 / (1 + tolerance) <= sFreq <= 1 / (1 - tolerance):
            continue
        # Fine pitch coherence:
        #   |queAy-canAy*sFreq| <= eFine
        if not abs(query_triplet[1] - (reference_triplet[1] * sFreq)) <= e_fine:
            continue
        offset = reference_triplet[0] - (query_triplet[0] /sTime)
        filtered[reference_triplet[4]].append((offset, (sTime, sFreq)))


def lookup_record(cursor, audio_id):
    """
    Returns title of given audio_id
    """
    cursor.execute("""SELECT audio_title
                   FROM Audios
                  WHERE id = ?""", (audio_id,))
    title = cursor.fetchone()
    return title[0]


def outlier_removal(binned_item, results):
    means = np.mean(binned_item[3], axis=0)
    stds = np.std(binned_item[3], axis=0)
    items = [v for v in binned_item[3] if
             (means[0] - 2 * stds[0] <= v[0] <= means[0] + 2 * stds[0]) and
             (means[1] - 2 * stds[1] <= v[1] <= means[1] + 2 * stds[1])]
    results.append([binned_item[0], binned_item[1], means[0], means[1], len(items)])


def store_peaks(cursor, spectral_peaks, audio_id):
    """
    Store spectral peaks extracted from reference audios.

    Parameters:
        cursor : the current cursor of the database.
        spectral_peaks (List) : list of spectral peaks extracted from the reference audio.
        audio_id (int): id of the audio.

    """
    for i in spectral_peaks:
        cursor.execute("""INSERT INTO Peaks
                     VALUES (?,?,?)""", (audio_id, int(i[0]), int(i[1])))


def lookup_peak_range(cursor, audio_id, offset, e=3750):
    """
    Queries Peaks table for peaks of given recordid that are within
    3750 samples (15s) of the estimated offset value.
    """
    data = (offset, offset + e, audio_id)
    cursor.execute("""SELECT Px, Py
                   FROM Peaks
                  WHERE Px >= ? AND Px <= ?
                    AND audio_id = ?""", data)
    return [p for p in cursor.fetchall()]


def verify_peaks(match, reference_peaks, query_peaks, eX=18, eY=12):
    """
    Checks for presence of a given set of reference peaks in the
    query fingerprint's list of peaks according to time and
    frequency boundaries (eX and eY). Each reference peak is adjusted
    according to estimated sFreq/sTime from candidate filtering
    stage.
    Returns: validation score (num. valid peaks / total peaks)
    """
    validated = 0
    for i in reference_peaks:
        reference_peak = (i[0] - match[1], i[1])
        reference_peak_scaled = (reference_peak[0] * match[2], reference_peak[1] *match[3])
        lBound = bisect_left(query_peaks, (reference_peak_scaled[0] - eX, None))
        rBound = bisect_right(query_peaks, (reference_peak_scaled[0] + eX, None))
        for j in range(lBound, rBound):
            if not reference_peak_scaled[1] - eY <= query_peaks[j][1] <= reference_peak_scaled[1] + eY:
                continue
            else:
                validated += 1
    vScore = (float(validated) / len(reference_peaks))
    return vScore


class FingerprintManager(object):
    """
    A class to manager storing audio fingerprints to a reference fingerprint database and query for
    a matching audio given audio fingerprints extracted from the query audio.

    Attributes:
        db_path (String): A path for the reference audio fingerprints database.

    """

    def __init__(self, db_path):
        """
        A constructor for FingerprintManager class.

        Parameters:
            db_path (String): a path to reference audio fingerprints database.

        """
        self.db_path = db_path
        with sqlite3.connect(self.db_path) as conn:
            create_tables(conn)
        conn.close()

    def store(self, audio_fingerprints, spectral_peaks, audio_title):
        """
        A method to store reference audio fingerprints along with the audio title to the
        reference audio fingerprints database.

        Parameters:
            audio_fingerprints (List): List of reference audio fingerprints.
            spectral_peaks (List): List of spectral peaks extracted from spectrogram of the audio.
            audio_title (String): Title of the audio.

        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if not record_exists(cursor=cursor, audio_title=audio_title):
                audio_id = store_audio(cursor=cursor, audio_title=audio_title)
                store_peaks(cursor=cursor, spectral_peaks=spectral_peaks, audio_id=audio_id)
                for i in audio_fingerprints:
                    store_hash(cursor=cursor, geo_hash=i[0])
                    store_triplet(cursor=cursor, triplet=i[1], audio_id=audio_id)
        conn.commit()
        conn.close()

    def query_audio(self, audio_fingerprints, spectral_peaks):
        """
        A method to query for a matching audio given fingerprints of a query audio.

        Parameters:
            audio_fingerprints (List): List of fingerprints extracted from query audio.
            spectral_peaks (List): List of spectral peaks extracted from spectrogram of the audio.

        Returns:

        """
        match_candidates = self.find_matches(audio_fingerprints)
        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()
        if len(match_candidates) > 0:
            reference_peaks = lookup_peak_range(cursor=cursor, audio_id=match_candidates[0][0],
                                                offset=match_candidates[0][1])

            v_score = verify_peaks(match=match_candidates[0], reference_peaks=reference_peaks,
                                   query_peaks=spectral_peaks)
            print(match_candidates[0][0], match_candidates[0][1], len(reference_peaks),v_score)
            if v_score > 0.1:
                audio_title = lookup_record(cursor=cursor, audio_id=match_candidates[0][0])
                cursor.close()
                conn.close()
                return audio_title, match_candidates[0][2], match_candidates[0][1]
            else:
                return "No Match", 0
        else:
            return "No Match", 0

    def find_matches(self, audio_fingerprints):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        filtered = defaultdict(list)
        for i in audio_fingerprints:
            find_hash(cursor=cursor, hash_value=i[0])
            with np.errstate(divide='ignore', invalid='ignore'):
                filter_candidates(cursor=cursor, query_triplet=i[1], filtered=filtered)
        binned = {k: bin_times(v) for k, v in filtered.items()}
        binned_items = list()
        results = list()
        for k, v in binned.items():
            for j, m in v.items():
                # print(v)
                binned_items.append([k, j, len(m), m])
        for i in binned_items:
            outlier_removal(binned_item=i, results=results)
        sorted_binned = sorted(binned_items, key=operator.itemgetter(2), reverse=True)
        sorted_results = sorted(results, key=operator.itemgetter(4), reverse=True)
        # print(sorted_binned)
        # print("Results", sorted_results)
        cursor.close()
        conn.close()
        return sorted_results
