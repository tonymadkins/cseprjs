import numpy as np
import shared

d = 5

def main(l=128, article_path="./Data/data50.csv", label_path="./Data/label.csv", groups_path="./Data/groups.csv"):
    print("Running d={0}, l={1}".format(d, l))
    print("Importing data")
    k = shared.setup(article_path, label_path, groups_path)
    hashtables = [HashFunction(d, k) for i in range(l)]
    print("Storing article hashes")
    articles_list = shared.generate_article_list()
    for ind, article in enumerate(articles_list):
        print("\tStoring {0} of {1} articles".format(ind + 1, len(articles_list)))
        for ht in hashtables:
            ht.store(article)

    print("Classifying articles")
    correct = 0
    match_set_size = 0
    for ind, article in enumerate(articles_list):
        print("\tClassifying {0} of {1} articles".format(ind + 1, len(articles_list)))
        match_set = get_matches(hashtables, article)
        match_set_size += len(match_set)
        match = shared.find_nearest_neighbor(match_set, article)
        if(match != None and match.group_id == article.group_id):
            correct += 1
    print("Classification results : {0} / {1}".format(correct, len(articles_list)))
    print("Classification error pct : {0}".format(100 * (len(articles_list) - correct) / len(articles_list)))
    print("Average set size : {0}".format(match_set_size / len(articles_list)))

def get_matches(hts, article):
    s = dict()
    for ht in hts:
        bkt = ht.buckets[ht.to_int(ht.hash_val(ht.to_vector(article.word_counts)))]
        for match in bkt:
            if(match.id != article.id):
                s[match.id] = match
    return list(s.values())

class HashFunction:
    def __init__(self, d, k):
        self.d = d
        self.k = k
        self.buckets = dict()
        self.m = np.random.normal(0.0, 1.0, (d, k))

    def store(self, article):
        hv = self.to_int(self.hash_val(self.to_vector(article.word_counts)))
        if(hv in self.buckets):
            self.buckets[hv].append(article)
        else:
            self.buckets[hv] = []
            self.buckets[hv].append(article)

    def hash_val(self, v):
        return (np.sign(np.matmul(self.m, v)) + 1) / 2

    def to_int(self, bits):
        out = 0
        for bit in bits:
            out = (out << 1) | int(bit)
        return out
    
    def to_vector(self, words):
        v = np.zeros(self.k)
        for word in words.keys():
            v[int(word) - 1] = words[word]
        return v

if __name__ == '__main__':
    main()