package ar.org.hclass.cath;

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


public class CathMapperTest extends CustomMapperTest {
	String filepath;

	@Before
	public void setUp() throws IOException{
		filepath =setUp( "1go5A00     1    10     8    10     1     1     1     1     2    69 999.000").getAbsolutePath();
		
	}
	
	/**
	 * @throws IOException
	 */
	@Test
	public void  testMock() throws IOException{
		CathMapper scopCathMapper = new CathMapper(); 
		LineMap<CathInfo> lineMap = new LineMap<CathInfo>(filepath, "utf-8",scopCathMapper);
		MapResult<CathInfo> map = lineMap.map();
		ArrayList<CathInfo> results = map.getResults();
		TestCase.assertEquals(1,results.size());
		CathInfo cathInfo = results.get(0);
		TestCase.assertEquals( "1go5A00",cathInfo.getId());
		TestCase.assertEquals( "1.10.8.10.1.1.1.1.2",cathInfo.getClassification());
	}


}
