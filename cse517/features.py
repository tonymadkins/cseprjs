class Features:
    fv = list()
    wordCount = {}
    tagWordCount = {}
    tagTagCount = {}
    tagPosCount = {}
    tagChunkCount = {}

    def f0(self, sentence, i, prevTag, tag):
        # the word count for O
        if sentence[i][0] in self.wordCount and tag == 'O':
            return self.wordCount[sentence[i][0]] / self.wordCount['_TOTAL_']
        return 0

    def f1(self, sentence, i, prevTag, tag):
        # the word count for I-PER
        if sentence[i][0] in self.wordCount and (tag == 'I-PER' or tag == 'B-PER'):
            return self.wordCount[sentence[i][0]] / self.wordCount['_TOTAL_']
        return 0
    
    def f2(self, sentence, i, prevTag, tag):
        # the word count for I-LOC
        if sentence[i][0] in self.wordCount and (tag == 'I-LOC' or tag == 'B-LOC'):
            return self.wordCount[sentence[i][0]] / self.wordCount['_TOTAL_']
        return 0

    def f3(self, sentence, i, prevTag, tag):
        # the word count for I-ORG
        if sentence[i][0] in self.wordCount and (tag == 'I-ORG' or tag == 'B-ORG'):
            return self.wordCount[sentence[i][0]] / self.wordCount['_TOTAL_']
        return 0

    def f4(self, sentence, i, prevTag, tag):
        # the word count for I-MISC
        if sentence[i][0] in self.wordCount and (tag == 'I-MISC' or tag == 'B-MISC'):
            return self.wordCount[sentence[i][0]] / self.wordCount['_TOTAL_']
        return 0

    def f5(self, sentence, i, prevTag, tag):
        # the previous word count given tag
        if i > 0:
            if tag in self.tagWordCount:
                if sentence[i-1][0] in self.tagWordCount[tag]:
                    return self.tagWordCount[tag][sentence[i-1][0]] / self.tagWordCount[tag]['_TOTAL_']
        return 0

    def f6(self, sentence, i, prevTag, tag):
        # the word tag count
        if tag in self.tagWordCount:
            if sentence[i][0] in self.tagWordCount[tag]:
                return self.tagWordCount[tag][sentence[i][0]] / self.tagWordCount[tag]['_TOTAL_']
        return 0
        
    def f7(self, sentence, i, prevTag, tag):
        # the pos tag count
        if tag in self.tagPosCount:
            if sentence[i][1] in self.tagPosCount[tag]:
                return self.tagPosCount[tag][sentence[i][1]] / self.tagPosCount[tag]['_TOTAL_']
        return 0
        
    def f8(self, sentence, i, prevTag, tag):
        # the chunk tag count
        if tag in self.tagChunkCount:
            if sentence[i][2] in self.tagChunkCount[tag]:
                return self.tagChunkCount[tag][sentence[i][2]] / self.tagChunkCount[tag]['_TOTAL_']
        return 0
        
    def f9(self, sentence, i, prevTag, tag):
        # the tag tag count
        if tag in self.tagTagCount:
            if prevTag in self.tagTagCount[tag]:
                return self.tagTagCount[tag][prevTag] / self.tagTagCount[tag]['_TOTAL_']
        return 0

    def f10(self, sentence, i, prevTag, tag):
        if sentence[i][1] == 'NNP' and sentence[i][2] == 'I-NP' and (tag == 'I-LOC' or tag == 'B-LOC'):
            return 1
        else:
            return 0
            
    def f11(self, sentence, i, prevTag, tag):
        if sentence[i][1] == 'NNP' and sentence[i][2] == 'I-NP' and (tag == 'I-PER' or tag == 'B-PER'):
            return 1
        else:
            return 0
            
    def f12(self, sentence, i, prevTag, tag):
        if sentence[i][1] == 'NNP' and sentence[i][2] == 'I-NP' and (tag == 'I-ORG' or tag == 'B-ORG'):
            return 1
        else:
            return 0
            
    def f13(self, sentence, i, prevTag, tag):
        if sentence[i][1] == 'NNP' and sentence[i][2] == 'I-NP' and (tag == 'I-MISC' or tag == 'B-MISC'):
            return 1
        else:
            return 0
            
    def f14(self, sentence, i, prevTag, tag):
        if sentence[i][1] == 'NNP' and sentence[i][2] == 'I-NP' and tag == 'O':
            return 1
        else:
            return 0

    def f15(self, sentence, i, prevTag, tag):
        if sentence[i][0].lower() in self.wordCount and (tag == 'I-LOC' or tag == 'B-LOC'):
            return 1
        else:
            return 0
            
    def f16(self, sentence, i, prevTag, tag):
        if sentence[i][0].lower() in self.wordCount and (tag == 'I-PER' or tag == 'B-PER'):
            return 1
        else:
            return 0
            
    def f17(self, sentence, i, prevTag, tag):
        if sentence[i][0].lower() in self.wordCount and (tag == 'I-ORG' or tag == 'B-ORG'):
            return 1
        else:
            return 0
            
    def f18(self, sentence, i, prevTag, tag):
        if sentence[i][0].lower() in self.wordCount and (tag == 'I-MISC' or tag == 'B-MISC'):
            return 1
        else:
            return 0
            
    def f19(self, sentence, i, prevTag, tag):
        if sentence[i][0].lower() in self.wordCount and tag == 'O':
            return 1
        else:
            return 0

    def f20(self, sentence, i, prevTag, tag):
        # the previous pos count given tag
        if i > 0:
            if tag in self.tagPosCount:
                if sentence[i-1][1] in self.tagPosCount[tag]:
                    return self.tagPosCount[tag][sentence[i-1][1]] / self.tagPosCount[tag]['_TOTAL_']
        return 0

    def f21(self, sentence, i, prevTag, tag):
        if i > 0 and sentence[i][0][0].isupper() and (tag == 'O' or tag == 'O'):
            return 1
        return 0
        
    def f22(self, sentence, i, prevTag, tag):
        if i > 0 and sentence[i][0][0].isupper() and (tag == 'I-PER' or tag == 'B-PER'):
            return 1
        return 0
        
    def f23(self, sentence, i, prevTag, tag):
        if i > 0 and sentence[i][0][0].isupper() and (tag == 'I-LOC' or tag == 'B-LOC'):
            return 1
        return 0
        
    def f24(self, sentence, i, prevTag, tag):
        if i > 0 and sentence[i][0][0].isupper() and (tag == 'I-MISC' or tag == 'B-MISC'):
            return 1
        return 0
        
    def f25(self, sentence, i, prevTag, tag):
        if i > 0 and sentence[i][0][0].isupper() and (tag == 'I-ORG' or tag == 'B-ORG'):
            return 1
        return 0

    def f26(self, sentence, i, prevTag, tag):
        if i > 0 and sentence[i][0][0].isupper() and sentence[i][2] == 'I-NP' and (tag == 'O' or tag == 'O'):
            return 1
        return 0
        
    def f27(self, sentence, i, prevTag, tag):
        if i > 0 and sentence[i][0][0].isupper() and sentence[i][2] == 'I-NP' and (tag == 'I-PER' or tag == 'B-PER'):
            return 1
        return 0
        
    def f28(self, sentence, i, prevTag, tag):
        if i > 0 and sentence[i][0][0].isupper() and sentence[i][2] == 'I-NP' and (tag == 'I-LOC' or tag == 'B-LOC'):
            return 1
        return 0
        
    def f29(self, sentence, i, prevTag, tag):
        if i > 0 and sentence[i][0][0].isupper() and sentence[i][2] == 'I-NP' and (tag == 'I-MISC' or tag == 'B-MISC'):
            return 1
        return 0
        
    def f30(self, sentence, i, prevTag, tag):
        if i > 0 and sentence[i][0][0].isupper() and sentence[i][2] == 'I-NP' and (tag == 'I-ORG' or tag == 'B-ORG'):
            return 1
        return 0