package ar.org.hclass;

import ar.org.facuq.linemap.Mapper;
import ar.org.facuq.linemap.ParsingLineException;
import ar.org.hclass.ScopCathInfo.ClassificationInfo;

/**
 * @author facundoq
 * Parses files of the format:
 * #More Info at: PLoS Comput Biol 5(3): e1000331. doi:10.1371/journal.pcbi.1000331
#Columns 1-5: SCOP domain, #residues and its codes for the different levels at SCOP 
#Columns 6-10: equivalent CATH domain, #residues and its codes for the different levels at CATH
#SCOP-dom Nres Fold Superf Family CATH-dom Nres Fold Superf Family 
1a6m__ 151 46458 46457 46463 1a6m000 151 11049010 110490 110490101
1allb_ 161 46458 46457 46532 1kn1B00 161 11049020 110490 110490203
1ash__ 147 46458 46457 46463 1ash000 147 11049010 110490 1104901020
1b0b__ 141 46458 46457 46463 1b0b000 141 11049010 110490 110490108
1cg5b_ 141 46458 46457 46463 1cg5B00 141 11049010 110490 1104901014
1cqxa1 150 46458 46457 46463 1cqxA01 150 11049010 110490 1104901015
1dlwa_ 116 46458 46457 46459 1dlwA00 116 11049010 110490 1104901022

 *
 */
public class ScopCathMapper implements Mapper<ScopCathInfo>{

	
	@Override
	public ScopCathInfo map(String content, Long number)
			throws ParsingLineException {
		String[] split = content.split( " ");
		ClassificationInfo scop=new ClassificationInfo(split[0], split[1], split[2], split[3], split[4]);
		ClassificationInfo cath=new ClassificationInfo(split[5], split[6], split[7], split[8], split[9]);
		return new ScopCathInfo(scop, cath);
	}

	@Override
	public boolean process(String line, Long number) {
		return !line.startsWith( "#");
	}
	
}
