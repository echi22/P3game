package ar.org.hclass.scop;

import java.util.HashMap;

import ar.org.facuq.linemap.Mapper;
import ar.org.facuq.linemap.ParsingLineException;

public class ScopMapper implements Mapper<Element>{
	
	HashMap<String, String> domainToFamily=new HashMap<String, String>();

	public HashMap<String, String> getDomainToFamily() {
		return domainToFamily;
	}

	@Override
	public Element map(String content, Long number)
			throws ParsingLineException {
		String[] split = content.split( "\t");
		if (split[1].equals( "px")){
			domainToFamily.put(split[3], split[2]);
		}
//TODO read element information 		
		return new Element();
	}

	@Override
	public boolean process(String line, Long number) {
		
		return !line.startsWith( "#");
	}
	
	

}
