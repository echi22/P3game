package ar.org.hclass;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import ar.org.facuq.linemap.LineMap;
import ar.org.facuq.linemap.MapResult;
import ar.org.facuq.utility.StringUtility;
import ar.org.facuq.utility.functional.Map;
import ar.org.facuq.utility.statistic.Histogram;
import ar.org.hclass.cath.CathInfo;
import ar.org.hclass.cath.CathMapper;
import ar.org.hclass.scop.Element;
import ar.org.hclass.scop.ScopMapper;

public class ScopCathFileGenerator {
	
	public static void main(String[] arguments ) throws IOException{
		HashMap<String, String> domainToScopFamily = domainToScopFamily();		
		HashMap<String, String> domainToCathFamily = domainToCathFamily();
		MapResult<ScopCathInfo> scopCathMapping = getScopCathMapping();
		
		ArrayList<ScopCathClassification> result=new ArrayList<ScopCathClassification>();
		ArrayList<String> missing=new ArrayList<String>();
		for (ScopCathInfo info : scopCathMapping.getResults()) {
			String scopFamily= domainToScopFamily.get( "d"+info.getScop().getDomain());
			if(scopFamily!= null){
			String cathClassification=  domainToCathFamily.get(info.getCath().getDomain());
			if(cathClassification!= null){
				ScopCathClassification c=new ScopCathClassification(info.getScop().getDomain(), scopFamily, info.getCath().getDomain(),cathClassification);
				
				result.add(c);
					
			}else{
				missing.add( "#domain  (Scop:"+ info.getScop().getDomain()+", cath: "+ info.getCath().getDomain()+") does not have a family identifier in cath (tentative family identifier: "+ info.getCath().getL3()+ ").");	
			}
			} else{
				missing.add( "#domain  "+ info.getScop().getDomain()+" does not have a family assigned in the current scop database.");
			}
			
		}
		System.out.println( "results ("+result.size()+ ") : "+result);
		System.out.println("missing ("+missing.size()+ ") : "+missing);
		for (ScopCathClassification c: result) {
			String  line=c.getScopId()+ " "+ c.getScopClassification()+ " ";
			line+=c.getCathId()+" "+c.getCathClassification();
			System.out.println(line);
		}
		showHistogram(result );
	}

	private static void showHistogram(ArrayList<ScopCathClassification> result) {
		Histogram<String> sHistogram= generateScopHistogram(result);
		Histogram<String> cHistogram= generateCathHistogram(result);
		System.out.println(result.size());
		System.out.println( "Scop: items that occurred more than once: "+sHistogram.itemsThatOccurredMoreThan(5)+ "( "+sHistogram.getItems().size()+" total)");
		System.out.println( "Cath: items that occurred more than once: "+cHistogram.itemsThatOccurredMoreThan(5)+ "( "+cHistogram.getItems().size()+" total)");
	}
	
	private static Histogram<String> generateScopHistogram(ArrayList<ScopCathClassification> items){
		return new Histogram<String>(new Map<ScopCathClassification,String>() {
			protected String map(ScopCathClassification c) {
//				int last =StringUtility.indexOf(c.getScopClassification(),'.',4);
//				return c.getScopClassification().substring(0, last);
				return c.getScopClassification();
			}
			
		}.map(items));
	}
	private static Histogram<String> generateCathHistogram(ArrayList<ScopCathClassification> items){
		return new Histogram<String>(new Map<ScopCathClassification,String>() {
			protected String map(ScopCathClassification c) {
				int last =StringUtility.indexOf(c.getCathClassification(),'.',2);
				return c.getCathClassification().substring(0, last);
//				return c.getCathClassification();
			}
			
		}.map(items));
	}

	private static HashMap<String, String> domainToCathFamily() throws IOException {
		CathMapper scopMapper = new CathMapper();
		LineMap<CathInfo> lineMap = new LineMap<CathInfo>("CathDomainList.txt", "utf-8",scopMapper);
		MapResult<CathInfo> map = lineMap.map();
		HashMap<String, String> domainToFamily =new HashMap<String, String>();
		for (CathInfo info : map.getResults()) {
			domainToFamily.put(info.getId(), info.getClassificationUpToLevel(5));
		}
		return domainToFamily;
	}

	private static MapResult<ScopCathInfo> getScopCathMapping()
			throws IOException {
		LineMap<ScopCathInfo> scopCathMap = new LineMap<ScopCathInfo>( "SCOP-CATH_Domain_Consens.dat",  "utf-8", new ScopCathMapper());
		MapResult<ScopCathInfo> map2 = scopCathMap.map();
		return map2;
	}

	private static HashMap<String, String> domainToScopFamily() throws IOException {
		ScopMapper scopMapper = new ScopMapper();
		LineMap<Element> lineMap = new LineMap<Element>("dir.des.scop_1.75.txt", "utf-8",scopMapper);
		MapResult<Element> map = lineMap.map();
		HashMap<String, String> domainToFamily = scopMapper.getDomainToFamily();
		return domainToFamily;
	}

//	/**
//	 * @param code
//	 * @return  the code with dots added  in the proper  positions
//	 */
//	private static String formatCathFamilyClassificationCode(String  code) {
//		String  result= code.substring(0,1)+ ".";
//		 result+=code.substring(1, 3)+ ".";
//		 result+=code.substring(3, 6)+ ".";
//		 result+=code.substring(6, 8)+ ".";
//		 result+=code.substring(8, code.length());
//		return   result;
//	}
}
