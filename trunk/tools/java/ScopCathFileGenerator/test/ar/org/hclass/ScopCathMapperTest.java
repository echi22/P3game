package ar.org.hclass;

import java.io.IOException;
import java.util.ArrayList;

import junit.framework.TestCase;

import org.junit.Before;
import org.junit.Test;

import ar.org.facuq.linemap.CustomMapperTest;
import ar.org.facuq.linemap.LineMap;
import ar.org.facuq.linemap.MapResult;
import ar.org.hclass.ScopCathInfo;
import ar.org.hclass.ScopCathMapper;


public class ScopCathMapperTest extends CustomMapperTest {
	String filepath;

	@Before
	public void setUp() throws IOException{
		filepath =setUp( "1a6m__ 151 46458 46457 46463 1a6m000 151 11049010 110490 110490101").getAbsolutePath();
		
	}
	
	/**
	 * @throws IOException
	 */
	@Test
	public void  testMock() throws IOException{
		ScopCathMapper scopCathMapper = new ScopCathMapper(); 
		LineMap<ScopCathInfo> lineMap = new LineMap<ScopCathInfo>(filepath, "utf-8",scopCathMapper);
		MapResult<ScopCathInfo> map = lineMap.map();
		ArrayList<ScopCathInfo> results = map.getResults();
		TestCase.assertEquals(1,results.size());
		ScopCathInfo scopCathInfo = results.get(0);
		TestCase.assertEquals( "1a6m000",scopCathInfo.getCath().getDomain());
		TestCase.assertEquals( "11049010",scopCathInfo.getCath().getL1());
		TestCase.assertEquals( "110490",scopCathInfo.getCath().getL2());
		TestCase.assertEquals( "110490101",scopCathInfo.getCath().getL3());
		TestCase.assertEquals( "1a6m__",scopCathInfo.getScop().getDomain());
		TestCase.assertEquals( "46458",scopCathInfo.getScop().getL1());
		TestCase.assertEquals( "46457",scopCathInfo.getScop().getL2());
		TestCase.assertEquals( "46463",scopCathInfo.getScop().getL3());
		
	}
}
