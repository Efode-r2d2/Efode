import math
import sqlite3
import numpy as np
from bisect import bisect_left, bisect_right
from collections import defaultdict, namedtuple
import operator


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
                    record_id INTEGER,
                    Ax INTEGER, Ay INTEGER,
                    Bx INTEGER, By INTEGER,
                    FOREIGN KEY(hash_id) REFERENCES Hashes(id),
                    FOREIGN KEY(record_id) REFERENCES Records(id));""")


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
                          WHERE title = ?""", (audio_title,))
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


def store_triplet(cursor, triplet, audio_id):
    """

    :param cursor:
    :param triplet:
    :param audio_id:
    :return:
    """
    hash_id = cursor.lastrowid
    values = (hash_id, audio_id, int(triplet[0]), int(triplet[1]), int(triplet[2]), int(triplet[3]))
    cursor.execute("""INSERT INTO Quads
                         VALUES (?,?,?,?,?,?)""", values)


def __lookup_triplets__(conn, hash_ids):
    cursor = conn.cursor()
    cursor.execute("""SELECT Ax,Ay,Bx,By,recordid FROM Quads
                          WHERE hashid=?""", hash_ids)
    row = cursor.fetchone()
    cursor.close()
    return [row[0], row[1], row[2], row[3]], row[4]


def __bin_times__(l, binwidth=20, ts=4):
    """
    Takes list of rough offsets and bins them in time increments of
    binwidth. These offsets are stored in a dictionary of
    {binned time : [list of scale factors]}. Binned time keys with
    less than Ts scale factor values are filtered out.
    """
    d = defaultdict(list)
    for rough_offset in l:
        div = rough_offset[0] / binwidth
        binname = int(math.floor(div) * binwidth)
        d[binname].append((rough_offset[1][0], rough_offset[1][1]))
    return {k: v for k, v in d.items() if len(v) >= ts}


def __outlier_removal__(d):
    """
    Calculates mean/std. dev. for sTime/sFreq values,
    then removes any outliers (defined as mean +/- 2 * stdv).
    Returns list of final means.
    """
    means = np.mean(d, axis=0)
    stds = np.std(d, axis=0)
    d = [v for v in d if
         (means[0] - 2 * stds[0] <= v[0] <= means[0] + 2 * stds[0]) and
         (means[1] - 2 * stds[1] <= v[1] <= means[1] + 2 * stds[1])]
    return d


def __scales__(d):
    """
    Receives dictionary of {binned time : [scale factors]}
    Performs variance-based outlier removal on these scales. If 4 or more
    matches remain after outliers are removed, a list with form
    [(rough offset, num matches, scale averages)]] is created. This result
    is sorted by # of matches in descending order and returned.
    """
    o_rm = {k: __outlier_removal__(v) for k, v in d.items()}
    res = [(i[0], len(i[1]), np.mean(i[1], axis=0))
           for i in o_rm.items() if len(i[1]) >= 4]
    sorted_mc = sorted(res, key=operator.itemgetter(1), reverse=True)
    return sorted_mc


def __store_peaks__(curosr, spectral_peaks, record_id):
    """
    Stores peaks from reference fingerprint
    """
    for i in spectral_peaks:
        curosr.execute("""INSERT INTO Peaks
                     VALUES (?,?,?)""", (record_id, int(i[0]), int(i[1])))


def __filter_candidates__(conn, cursor, query_quad, filtered, tolerance=0.31, e_fine=1.8):
    for hash_ids in cursor:
        reference_quad, record_id = __lookup_triplets__(conn, hash_ids)
        # Rough pitch coherence:
        #   1/(1+e) <= queAy/canAy <= 1/(1-e)
        if not 1 / (1 + tolerance) <= query_quad[1] / reference_quad[1] <= 1 / (1 - tolerance):
            continue
        # X transformation tolerance check:
        #   sTime = (queBx-queAx)/(canBx-canAx)
        sTime = (query_quad[2] - query_quad[0]) / (reference_quad[2] - reference_quad[0])
        if not 1 / (1 + tolerance) <= sTime <= 1 / (1 - tolerance):
            continue
        # Y transformation tolerance check:
        #   sFreq = (queBy-queAy)/(canBy-canAy)
        sFreq = (query_quad[3] - query_quad[1]) / (reference_quad[3] - reference_quad[1])
        if not 1 / (1 + tolerance) <= sFreq <= 1 / (1 - tolerance):
            continue
        # Fine pitch coherence:
        #   |queAy-canAy*sFreq| <= eFine
        if not abs(query_quad[1] - (reference_quad[1] * sFreq)) <= e_fine:
            continue
        offset = reference_quad[0] - (query_quad[0] * sTime)
        filtered[record_id].append((offset, (sTime, sFreq)))


class DataManager(object):
    """
    A class to manager storing audio fingerprints to a reference fingerprint database and query for
    a matching audio given audio fingerprints extracted from the query audio.

    Attributes:
        db_path (String): A path for the reference audio fingerprints database.

    """

    def __init__(self, db_path):
        """
        A constructor for DataManager class.

        Parameters:
            db_path (String): a path to reference audio fingerprints database.

        """
        self.db_path = db_path
        with sqlite3.connect(self.db_path) as conn:
            create_tables(conn)
        conn.close()

    def store(self, audio_fingerprints, audio_title):
        """
        A method to store reference audio fingerprints along with the audio title to the
        reference audio fingerprints database.

        Parameters:
            audio_fingerprints (List): List of reference audio fingerprints.
            audio_title (String): Title of the audio.

        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if not record_exists(cursor=cursor, audio_title=audio_title):
                record_id = store_audio(cursor=cursor, audio_title=audio_title)
                for i in audio_fingerprints:
                    store_hash(cursor=cursor, geo_hash=i[0])
                    store_triplet(cursor=cursor, triplet=i[1], audio_id=record_id)
        conn.commit()
        conn.close()

    def __query__(self, audio_fingerprints):
        match_candidates = self.__find_match_candidates__(audio_fingerprints)
        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()
        if len(match_candidates) > 0 and match_candidates[0].num_matches > 5:
            print(self._lookup_record(c=cursor, recordid=match_candidates[0].recordid), match_candidates[0])
        else:
            print("No Match Found")
        cursor.close()
        conn.close()

    def __find_match_candidates__(self, audio_fingerprints):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        filtered = defaultdict(list)
        for i in audio_fingerprints:
            radius_nn(cursor, i[0])
            with np.errstate(divide='ignore', invalid='ignore'):
                __filter_candidates__(conn, cursor, i[1], filtered)
        binned = {k: __bin_times__(v) for k, v in filtered.items()}
        results = {k: __scales__(v)
                   for k, v in binned.items() if len(v) >= 4}
        match_candidates = [self.MatchCandidate(k, a[0], a[1], a[2][0], a[2][1])
                            for k, v in results.items() for a in v]
        cursor.close()
        conn.close()
        sorted_match = sorted(match_candidates, key=operator.itemgetter(2), reverse=True)
        return sorted_match

    def _validate_match(self, spectral_peaks, cursor, match_candidate):
        """
        """
        rPeaks = self._lookup_peak_range(cursor, match_candidate.recordid, match_candidate.offset)
        vScore = self._verify_peaks(match_candidate, rPeaks, spectral_peaks)
        return self.Match(self._lookup_record(cursor, match_candidate.recordid), match_candidate.offset, vScore)

    def _lookup_peak_range(self, c, recordid, offset, e=3750):
        """
        Queries Peaks table for peaks of given recordid that are within
        3750 samples (15s) of the estimated offset value.
        """
        data = (offset, offset + e, recordid)
        c.execute("""SELECT X, Y
                       FROM Peaks
                      WHERE X >= ? AND X <= ?
                        AND recordid = ?""", data)
        return [self.Peak(p[0], p[1]) for p in c.fetchall()]

    def _verify_peaks(self, mc, rPeaks, qPeaks, eX=18, eY=12):
        """
        Checks for presence of a given set of reference peaks in the
        query fingerprint's list of peaks according to time and
        frequency boundaries (eX and eY). Each reference peak is adjusted
        according to estimated sFreq/sTime from candidate filtering
        stage.
        Returns: validation score (num. valid peaks / total peaks)
        """
        validated = 0
        for rPeak in rPeaks:
            rPeak = (rPeak.x - mc.offset, rPeak.y)
            rPeakScaled = self.Peak(rPeak[0] / mc.sFreq, rPeak[1] / mc.sTime)
            lBound = bisect_left(qPeaks, (rPeakScaled.x - eX, len(qPeaks)))
            rBound = bisect_right(qPeaks, (rPeakScaled.x + eX, len(qPeaks)))
            for i in range(lBound, rBound):
                if not rPeakScaled.y - eY <= qPeaks[i][1] <= rPeakScaled.y + eY:
                    continue
                else:
                    validated += 1
        if len(rPeaks) == 0:
            vScore = 0.0
        else:
            vScore = (float(validated) / len(rPeaks))
        return vScore

    def _lookup_record(self, c, recordid):
        """
        Returns title of given recordid
        """
        c.execute("""SELECT title
                       FROM Records
                      WHERE id = ?""", (recordid,))
        title = c.fetchone()
        return title[0]
