package ar.org.hclass.cath;

import ar.org.facuq.linemap.Mapper;
import ar.org.facuq.linemap.ParsingLineException;
import ar.org.hclass.ScopCathInfo.ClassificationInfo;

/**
 * @author facundoq
 * Parses files of the format:
 *# FILE FORMAT:  Cath List File (CLF) Format 2.0
#
# FILE DESCRIPTION:
# Contains all classified protein domains in CATH
# for class 1 (mainly alpha), class 2 (mainly beta),
# class 3 (alpha and beta) and class 4 (few secondary structures).
#
# See 'README.file_formats' for file format information
#---------------------------------------------------------------------
1oaiA00     1    10     8    10     1     1     1     1     1    59 1.000
1go5A00     1    10     8    10     1     1     1     1     2    69 999.000
3frhA01     1    10     8    10     2     1     1     1     1    58 1.200
3friA01     1    10     8    10     2     1     1     1     2    54 1.800
3b89A01     1    10     8    10     2     1     1     2     1    54 2.600

 *
 */
public class CathMapper implements Mapper<CathInfo>{

	
	@Override
	public CathInfo map(String content, Long number)
			throws ParsingLineException {
		String id= content.substring(0, 12).trim();
		String classification= content.substring(12,65).trim().replaceAll( " +",  ".");
		return new CathInfo(id, classification);
	}

	@Override
	public boolean process(String line, Long number) {
		return !line.startsWith( "#");
	}
	
}
