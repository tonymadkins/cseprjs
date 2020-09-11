from quickhash import QuickHash
import numpy as np

def main():
    p = 10007 # big prime
    b = 256 # counters/buckets
    l = 4 # number of hash functions    

    stream = build_stream("FWD")
    stream_rev = build_stream("REV")
    stream_rand = build_stream("RAND")

    # for each stream
    est = estimates(stream, p, b, l)
    #print(0.01 * len(est))
    print('2050 forward estimate: ' + str(est[2049]))
    print(hhcount(est, 0.01 * len(est)))
    est_rev = estimates(stream_rev, p, b, l)
    print('2050 reverse estimate: ' + str(est_rev[2049]))
    print(hhcount(est_rev, 0.01 * len(est_rev)))
    est_rand = estimates(stream_rand, p, b, l)
    print('2050 random estimate: ' + str(est_rand[2049]))
    print(hhcount(est_rand, 0.01 * len(est_rand)))

def estimates(stream, p, b, l):
    trials = 10
    est = np.zeros(9050, dtype=int)
    # for each trial
    for t in np.arange(0, trials):
        hfs = []
        tbls = []
        # initialize hash functions and table
        for j in np.arange(0, l):
            hfs.append(QuickHash(np.random.randint(1, p), np.random.randint(0, p), p, b))
            tbls.append(np.zeros(b, dtype=int))
        # process stream
        for s in stream:
            # calculate each hash and increment
            for j in np.arange(0, l):
                tbls[j][hfs[j].hash(s)] += 1
        # get count estimates
        for i in np.arange(0, 9050):
            est[i] += min(tbls[j][hfs[j].hash(i + 1)] for j in np.arange(0, l))
    return est / trials

def hhcount(est, min):
    ct = 0
    for e in est:
        if e >= min:
            ct += 1
    return ct

def build_stream(mode):
    stream = []
    for i in np.arange(1, 10):
        for j in np.arange((1000 * (i - 1)) + 1, 1000 * i + 1):
            for k in np.arange(1, i + 1):
                stream.append(j)
    for i in np.arange(1, 51):
        for j in np.arange(1, (i^2) + 1):
            stream.append(9000 + i)

    if mode == "REV":
        np.flip(stream, axis=0)
    if mode == "RAND":
        np.random.shuffle(stream)
    return stream


if __name__ == "__main__":
    main()
