package ar.org.hclass.cath;

import ar.org.facuq.utility.StringUtility;

public class CathInfo {
String id, classification;

public CathInfo(String id, String classification) {
	super();
	this.id = id;
	this.classification = classification;
}

public String getId() {
	return id;
}

public String getClassification() {
	return classification;
}

public String getClassificationUpToLevel(int level ){
	int index=StringUtility.indexOf(classification,  '.', level );
	return classification.substring(0, index);
}

}
