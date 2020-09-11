package hw1;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

public class FileProcessor {

	final static String START = "__START__";
	final static String START2 = "__START2__";
	final static String STOP = "__STOP__";
	
	public static List<String[]> GetData(
		String dirName,
		String fileName)
	{
		var data = new ArrayList<String[]>();
		try (Stream<String> stream = Files.lines(Paths.get(dirName + fileName))) {
			stream.forEach(
					line -> data.add(
						(START + " " + START2 + " " + line.replaceAll("[^a-zA-Z ]", " ") + " " + STOP)
							.split("\\s+")));
		} catch (IOException e) {
			e.printStackTrace();
		}
		return data;
	}

}
