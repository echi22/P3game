package ar.org.hclass;

public class ScopCathClassification {
	String scopId;
	String scopClassification;
	String cathId;
	String cathClassification;
	public String getScopId() {
		return scopId;
	}
	public String getScopClassification() {
		return scopClassification;
	}
	public String getCathId() {
		return cathId;
	}
	public String getCathClassification() {
		return cathClassification;
	}
	public ScopCathClassification(String scopId, String scopClassification,
			String cathId, String cathClassification) {
		super();
		this.scopId = scopId;
		this.scopClassification = scopClassification;
		this.cathId = cathId;
		this.cathClassification = cathClassification;
	}

}
