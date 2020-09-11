package hw1;

import java.util.HashMap;
import java.util.Map;

public class Program {
	
	final static String DIR_NAME = ".\\CSE517-HW1-Data\\prob1_brown_full\\";
	final static String DEV_TEXT_FILE_NAME = "brown.dev.txt";
	final static String TRAIN_TEXT_FILE_NAME = "brown.train.txt";
	final static String TEST_TEXT_FILE_NAME = "brown.test.txt";

	public static void main(String[] args) throws Exception {
		double a = 0.0;
		double b = 0.0;
		double c = 0.0;
		Map<Double, Double> kVals = null;
		
		if(args[0].equalsIgnoreCase("a")) {
			// alpha params
			a = Double.parseDouble(args[1]);
			b = Double.parseDouble(args[2]);
			c = Double.parseDouble(args[3]);
		}else if(args[0].equalsIgnoreCase("k")){
			kVals = SetupKVals();
		}
		
		System.out.println("Importing Training Data");
		var ngramProc = new NGramProcessor(DIR_NAME, TRAIN_TEXT_FILE_NAME);
		ngramProc.InitTrain(true, a, b, c);
		System.out.println("Assert a valid probability distribution");
		
		// Validate the probability distribution
		// Commented out for performance
		//ngramProc.ValidateMLProbabilityDistribution();
		//ngramProc.ValidateLIProbabilityDistribution();
		
		System.out.println("Importing Test Data");
		//var testData = FileProcessor.GetData(DIR_NAME, TRAIN_TEXT_FILE_NAME);
		//var testData = FileProcessor.GetData(DIR_NAME, DEV_TEXT_FILE_NAME);
		var testData = FileProcessor.GetData(DIR_NAME, TEST_TEXT_FILE_NAME);
		ngramProc.InitTest(testData);
		
		//double p1 = ngramProc.Perplexity(testData, 1);
		//System.out.printf("p1: %f\n", p1);
		//double p2 = ngramProc.Perplexity(testData, 2);
		//System.out.printf("p2: %f\n", p2);
		Map<Double, Double> p3 = ngramProc.Perplexity(testData, 3, kVals);
		for(Double k : p3.keySet()) {
			System.out.println("K(" + k + "): " + p3.get(k));
		}
		//System.out.printf("p3: %f\n", p3);
	}

	private static HashMap<Double, Double> SetupKVals() {
		var kVals = new HashMap<Double, Double>();
		kVals.put(0.001d, 0d);
		kVals.put(0.003d, 0d);
		kVals.put(0.006d, 0d);
		kVals.put(0.01d, 0d);
		kVals.put(0.03d, 0d);
		kVals.put(0.06d, 0d);
		kVals.put(0.1d, 0d);
		kVals.put(0.3d, 0d);
		kVals.put(0.6d, 0d);
		kVals.put(1.0d, 0d);
		kVals.put(2.0d, 0d);
		kVals.put(5.0d, 0d);
		kVals.put(10.0d, 0d);
		kVals.put(20.0d, 0d);
		return kVals;
	}
}
