package hw1;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class NGramProcessor {
	final String UNK = "<UNK>";
	final int UNK_LIMIT = 3;
	
	boolean useUnk;
	double a;
	double b;
	double c;
	long trainWordCount;
	List<String[]> data;
	Map<String, Long> unigramCounts;
	Map<String, Long> bigramCounts;
	Map<String, Long> trigramCounts;
	
	NGramProcessor(String dir, String file){
		this.data = FileProcessor.GetData(dir, file);
		this.trainWordCount = 0;
	}

	public void InitTest(List<String[]> testData) {
		// Replace unseen words in test with UNK
		if(this.useUnk) {
			for(int i = 0; i < testData.size(); i++) {
				String[] line = testData.get(i);
				for(int j = 0; j < line.length; j++) {
					if(!this.unigramCounts.containsKey(ToGramKey(line[j]))){
						line[j] = UNK;
					}
				}
				testData.set(i, line);
			}
		}		
	}
	
	public void InitTrain(boolean useUnk, double a, double b, double c) {		
		// *** PRE-PROCESSING *** 
		this.useUnk = useUnk;
		this.a = a;
		this.b = b;
		this.c = c;
		if(this.useUnk) {
			// Replace rare words with UNK
			var counts = GetCounts(this.data, 1);
			for(int i = 0; i < this.data.size(); i++) {
				String[] line = this.data.get(i);
				for(int j = 0; j < line.length; j++) {
					if(counts.get(ToGramKey(line[j])) <= UNK_LIMIT){
						line[j] = UNK;
					}
				}
				this.data.set(i, line);
			}
		}
		
		// Get counts for total words, unigrams, bigrams, and trigrams
		this.unigramCounts = GetCounts(this.data, 1);
		this.bigramCounts = GetCounts(this.data, 2);
		this.trigramCounts = GetCounts(this.data, 3);
		this.trainWordCount = this.unigramCounts.values().stream().mapToLong(l -> l).sum();
	}
	
	Map<Double, Double> Perplexity(List<String[]> testData, int n, Map<Double, Double> kSet) {
		long testWordCount = testData.stream().mapToLong(li -> li.length).sum();
		Map<Double, Double> klogProb = new HashMap<Double, Double>(); // log2(p(s))
		if(kSet != null) {
			for(Double k : kSet.keySet()) {
				klogProb.put(k, 0d);
			}
		}
		
		double logProb = 0d;
		for(String[] line : testData) {
			 for(int i = 0; i < line.length - n + 1; i++){
				 String gram = ToGramKey(Arrays.copyOfRange(line, i, i + n));
				 String gramMinusOne = ToGramKey(Arrays.copyOfRange(line, i, i + n - 1));
				 String gramMinusTwo = ToGramKey(Arrays.copyOfRange(line, i, i + n - 2));
				 Map<Double, Double> kprob = new HashMap<Double, Double>();
				 double prob = 0d;
				 switch(n) {
				 	case 1: // UNIGRAM
				 		if(!this.unigramCounts.containsKey(gram)){
				 			gram = ToGramKey(UNK);
				 		}
				 		prob = ML(gram, gramMinusOne, n);
				 		logProb += Math.log(prob) / Math.log(2);
				 		break;
				 	case 2: // BIGRAM
				 		prob = ML(gram, gramMinusOne, n);
				 		logProb += Math.log(prob) / Math.log(2);
				 		break;
				 	case 3: // TRIGRAM
				 		if(kSet != null) {
					 		kprob = KSmoothed(gram, gramMinusOne, n, kSet);
					 		for(Double k : kSet.keySet()) {
					 			klogProb.put(k, klogProb.get(k) + Math.log(kprob.get(k) / Math.log(2)));
					 		}
				 		}else {
					 		prob = LI(gram, gramMinusOne, gramMinusTwo);
					 		logProb += Math.log(prob) / Math.log(2);
				 		}

				 		break;
				 }
			 }
		}
		
		if(n == 3 && kSet != null) {
			for(Double k : kSet.keySet()) {
				kSet.put(k, Math.pow(2, -(klogProb.get(k) / (double)testWordCount)));
			}
			return kSet; // 2^-l
		}
		
		
		var ret = new HashMap<Double, Double>();
		ret.put(0.0, Math.pow(2, -(logProb / (double)testWordCount)));
		return ret;
	}
	
	private double LI(String trigram, String bigram, String unigram) {
		// Linear interpolation
		double triML = ML(trigram, MinusOne(trigram), 3);
		double biML = ML(bigram, MinusOne(bigram), 2);
		double uniML = ML(unigram, null, 1);
		double sum = (this.a*triML) + (this.b*biML) + (this.c*uniML);
		//System.out.print(this.a + " * " + triML + " + " + this.b + " * " + biML + " + " + this.c + " * " + uniML + " = " + sum);
		return sum;
	}

	private String MinusOne(String gram) {
		List<String> pieces = Arrays.asList(gram.substring(1, gram.length() - 1).split(", "));
		List<String> minusOne = pieces.subList(0, pieces.size() - 1);
		return ToGramKey(minusOne.toArray(new String[0]));
	}

	private Map<Double, Double> KSmoothed(String gram, String gramMinusOne, int n,  Map<Double, Double> kSet) {
		Map<Double, Double> ret = new HashMap<Double, Double>();
		Map<Double, Double> denom = new HashMap<Double, Double>();
		Map<Double, Double> num = new HashMap<Double, Double>();
		for(Double k : kSet.keySet()) {
			num.put(k, k);
			denom.put(k, 0d);
		}
		switch(n) {
			case 3:
				if(this.trigramCounts.containsKey(gram)) {
					for(Double k : num.keySet()) {
						num.put(k, num.get(k) + this.trigramCounts.get(gram));
					}
				}
				for(Double k : denom.keySet()) {
					denom.put(k, denom.get(k) + k * this.unigramCounts.keySet().size());
				}
				for(String uni : this.unigramCounts.keySet()) {
					String tri = gramMinusOne.substring(0, gramMinusOne.length() - 1) + ", " + uni.substring(1, uni.length());
					if(this.trigramCounts.containsKey(tri)) {
						for(Double k : denom.keySet()) {
							denom.put(k, denom.get(k) + this.trigramCounts.get(tri));
						}
					}
				}
		}
		
		for(Double k : kSet.keySet()) {
			ret.put(k, num.get(k) / denom.get(k));
		}
		return ret;
	}
	
	private double ML(String gram, String gramMinusOne, int n) {
		switch(n) {
			case 1:
				if(this.unigramCounts.containsKey(gram)) {
					return (double)this.unigramCounts.get(gram) / (double)this.trainWordCount;
				}
			case 2:
				if(this.bigramCounts.containsKey(gram)) {
		 			return (double)this.bigramCounts.get(gram) / (double)this.unigramCounts.get(gramMinusOne);
		 		}
				break;
			case 3:
				if(this.trigramCounts.containsKey(gram)) {
		 			return (double)this.trigramCounts.get(gram) / (double)this.bigramCounts.get(gramMinusOne);
		 		}
				break;
		}
		
		return 0d;
	}

	Map<String, Long> GetCounts(List<String[]> data, int n){
		Map<String, Long> counts = new HashMap<String, Long>();
		for(String[] line : data){
			 for(int i = 0; i < line.length - n + 1; i++){
				 String gram = ToGramKey(Arrays.copyOfRange(line, i, i + n));
				 if(!counts.containsKey(gram)) {
					 counts.put(gram, (long) 1);
				 }
				 else {
					 counts.put(gram, counts.get(gram) + 1);
				 }
			 }
		}
		return counts;
	}
	
	String ToGramKey(String ...args){
		return Arrays.toString(args);
	}

	public void ValidateMLProbabilityDistribution() throws Exception {
		// For each word, given 
		int current = 0;
		int total = this.bigramCounts.keySet().size();
		for(String bigram : this.bigramCounts.keySet()) {
			current++;
			if(current % 10000 == 0) {
				System.out.println(current + " / " + total);	
			}
			if(!bigram.contains(FileProcessor.STOP)) { // skip STOP bc nothing follows STOP
				double prob = 0d;
				for(String unigram : this.unigramCounts.keySet()) {
					String word = unigram.substring(1, unigram.length() - 1);
					String trigram = bigram.substring(0, bigram.length() - 1) + ", " + word + "]";
					if(this.trigramCounts.containsKey(trigram)) {
						prob += (double)this.trigramCounts.get(trigram) / (double)this.bigramCounts.get(bigram);
					}
				}
				// Make sure the probability is within 1e-10 of 1 (double rounding fails to be exactly 1.0)
				if(Math.abs(1d - prob) > 1e-10d) {
					throw new Exception("Prob " + prob + " does not equal 1 for bigram " + bigram);
				}
			}
		}
	}

	public void ValidateLIProbabilityDistribution() throws Exception {
		// For each word, given 
		int current = 0;
		int total = this.bigramCounts.keySet().size();
		for(String bigram : this.bigramCounts.keySet()) {
			String[] words = bigram.split(", ");
			String wordMinusTwo = words[0].substring(1, words[0].length());
			String wordMinusOne = words[1].substring(0, words[1].length() - 1);
			current++;
			if(current % 10000 == 0) {
				System.out.println(current + " / " + total);	
			}
			if(!bigram.contains(FileProcessor.STOP)) { // skip STOP bc nothing follows STOP
				double prob = 0;
				for(String unigram : this.unigramCounts.keySet()) {
					String word = unigram.substring(1, unigram.length() - 1);
					String trigram = ToGramKey(wordMinusTwo, wordMinusOne, word);
					String thisBi = ToGramKey(wordMinusOne, word);
					prob += LI(trigram, thisBi, unigram);
					if(prob > 1.1) {
						// throw early, throw often
						throw new Exception(trigram + ", " + thisBi + ", " + unigram + " : " + prob);
					}
				}
				// Make sure the probability is within 1e-10 of 1 (double rounding fails to be exactly 1.0)
				if(Math.abs(1d - prob) > 1e-10d) {
					throw new Exception("Prob " + prob + " does not equal 1 for bigram " + bigram);
				}
			}
		}
	}
}
