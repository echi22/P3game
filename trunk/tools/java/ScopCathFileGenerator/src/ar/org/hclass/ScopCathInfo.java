package ar.org.hclass;

public class ScopCathInfo {
	ClassificationInfo scop, cath;

	public ScopCathInfo(ClassificationInfo scop, ClassificationInfo cath) {
		super();
		this.scop = scop;
		this.cath = cath;
	}
	

	public ClassificationInfo getScop() {
		return scop;
	}


	public ClassificationInfo getCath() {
		return cath;
	}


	public static  class ClassificationInfo{

		String domain;
		String residue;
		String l1,l2,l3;
		public ClassificationInfo(String domain, String residue, String l1,
				String l2, String l3) {
			super();
			this.domain = domain;
			this.residue = residue;
			this.l1 = l1;
			this.l2 = l2;
			this.l3 = l3;
		}
		public String getDomain() {
			return domain;
		}
		public String getResidue() {
			return residue;
		}
		public String getL1() {
			return l1;
		}
		public String getL2() {
			return l2;
		}
		public String getL3() {
			return l3;
		}
		
	}
}
