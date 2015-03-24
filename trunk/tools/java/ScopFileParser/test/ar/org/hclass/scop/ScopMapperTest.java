package ar.org.hclass.scop;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

import junit.framework.TestCase;

import org.junit.Before;
import org.junit.Test;

import ar.org.facuq.linemap.LineMap;
import ar.org.facuq.linemap.MapResult;


public class ScopMapperTest {
	String filepath;

	@Before
	public void setUp() throws IOException{
		File temporary = File.createTempFile("scop", ".dat");
		filepath =temporary.getAbsolutePath();
	    // Delete temp file when program exits.
	    temporary.deleteOnExit();

	    // Write to temp file
	    BufferedWriter out = new BufferedWriter(new FileWriter(temporary));
	    out.write("14982	px	a.1.1.1	d1dlwa_	1dlw A:\n100068	px	a.1.1.1	d1uvya_	1uvy A:\n");
	    out.close();

	}
	
	/**
	 * @throws IOException
	 */
	@Test
	public void  testMock() throws IOException{
		ScopMapper scopMapper = new ScopMapper();
		LineMap<Element> lineMap = new LineMap<Element>(filepath, "utf-8",scopMapper);
		MapResult<Element> map = lineMap.map();
		ArrayList<Element> results = map.getResults();
		TestCase.assertEquals(2,scopMapper.domainToFamily.size());
		TestCase.assertEquals( "a.1.1.1",scopMapper.domainToFamily.get( "d1dlwa_"));
		TestCase.assertEquals( "a.1.1.1",scopMapper.domainToFamily.get( "d1uvya_"));
	}
	@Test
	public void  testScop() throws IOException{
		ScopMapper scopMapper = new ScopMapper();
		LineMap<Element> lineMap = new LineMap<Element>("dir.des.scop_1.75.txt", "utf-8",scopMapper);
		MapResult<Element> map = lineMap.map();
		ArrayList<Element> results = map.getResults();
//		System.out.println( scopMapper.domainToFamily.size());
		TestCase.assertEquals( "h.1.20.1",scopMapper.domainToFamily.get( "d1gk7a_"));
		
	}
}
